import asyncio
import json
import os
from typing import Any

import requests
from dotenv import load_dotenv
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langgraph.graph import add_messages, StateGraph, START, END

from tools import client
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_openai.chat_models import ChatOpenAI
from typing_extensions import TypedDict, Annotated
from fastapi import WebSocket, Request
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore
from functools import partial
from langchain.tools import tool

load_dotenv()

# 读取环境变量
API_KEY = os.getenv("API_KEY")
QQ_MAP_KEY = os.getenv("QQ_MAP_KEY")

# 模型参数传递
# tongyi = ChatTongyi(
#     model='qwen3-max',
#     api_key=API_KEY,
#     streaming=True
# )

tongyi = ChatOpenAI(
    model="qwen-plus-2025-12-01",
    api_key=API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 获取经纬度接口专用
tongyi_position = ChatTongyi(
    model='qwen-plus-2025-12-01',
    api_key=API_KEY
)


# tongyi = ChatOpenAI(
#     model="qwen-plus",
#     api_key=API_KEY,
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
#     streaming=True
# )

# 定义地图返回数据
@tool
def map_data(
        from_location: str,
        to_location: str,
        day: str,
        markers: list[Any],
        waypoints: str | list[Any] | None = None,
):
    """
    【核心功能】根据旅游攻略内容调用腾讯地图获取景点经纬度位置，并返回路线规划数据。

    【使用场景】
    例如旅游攻略：第一天：上午大理古城(起点)，下午洱海(途经点).....，晚上双廊古城(终点)；
    需为该天路线调用本工具，传入起点/终点/途经点经纬度，以及景点标记点信息。

    【参数要求（必须严格遵守）】
    1. from_location: 起点经纬度，格式为字符串，示例："25.812655,100.230119"（纬度在前，经度在后）
    2. to_location: 终点经纬度，格式同from_location，示例："25.700801,100.170478"
    3. day: 行程天数，字符串类型，示例："第一天"
    4. waypoints:字符串类型，可选，途经点，经纬度，多个用分号拼接："25.911703,100.203224;25.901234,100.203999"，若无途经点，返回None

    5. markers（关键！格式必须严格符合）:
       - 类型：Python列表（list），**禁止返回JSON字符串**
       - 列表内每个元素为字典，字典字段及类型要求：
         {
           "id": 数字类型（int，如12，需唯一，可使用时间戳）,
           "latitude": 数字类型（float，如25.812655）,
           "longitude": 数字类型（float，如100.203224）,
           "content": 字符串类型（如"大理古城"）
         }
       - 正确示例：
         [{"id":12,"latitude":25.812655,"longitude":100.203224,"content":"大理古城"}, {"id":13,"latitude":25.700801,"longitude":100.170478,"content":"洱海"}]
       - 错误示例（禁止）：
         '[{"id":12,"latitude":25.812655,"longitude":100.203224,"content":"大理古城"}]'（JSON字符串）

    【注意事项】
    1. 起点/终点/途经点经纬度需先调用bailian_web_search工具获取，本工具仅负责请求腾讯地图接口；
    2. 本工具仅处理单天路线，多天规划需多次调用后整合结果；
    3. 所有参数的字段类型、格式必须严格匹配上述要求，尤其是waypoints禁止返回列表、markers禁止返回字符串！
    """
    print("工具调用")
    print("from_location:", from_location)
    print("to_location:", to_location)
    print("day:", day)
    print("markers:", markers)
    print("waypoints:", waypoints)
    print("------------------")
    url = "https://apis.map.qq.com/ws/direction/v1/driving/"
    params = {
        "from": from_location,
        "to": to_location,
        "key": QQ_MAP_KEY,
    }
    if waypoints:
        if type(waypoints) != list:
            params["waypoints"] = waypoints
        else:
            params["waypoints"] = ",".join(str(num) for num in waypoints)
    res = requests.get(url, params=params)
    data = res.json()
    print('data--------')
    print(data)
    print('data--------')
    # 全部路线
    routes = data.get("result").get("routes", [])
    print('routes--------')
    print(routes)
    print('routes--------')
    if not routes or len(routes) < 1:
        return json.dumps({"points": [], "type": "route_polyline", "day": day, "marker": []})
    # 取第一条路线路径
    polyline = routes[0].get("polyline", [])
    print('polyline--------')
    print(polyline)
    print('polyline--------')
    # 坐标解压（返回的点串坐标，通过前向差分进行压缩）
    kr = 1000000.0
    pl = []
    for item in range(2, len(polyline)):
        polyline[item] = polyline[item - 2] + polyline[item] / kr
    # 将解压后的坐标放入点串数组pl中
    for item in range(0, len(polyline), 2):
        pl.append({"latitude": polyline[item], "longitude": polyline[item + 1]})
    return json.dumps(
        {"points": pl, "type": "route_polyline", "day": day, "marker": markers}
    )
# 工具类型
class ToolInfo(TypedDict):
    tools_by_name: dict[str, BaseTool]
    llm_with_tools: Runnable[LanguageModelInput, BaseMessage]
    all_tools: list[BaseTool]


# 定义状态
class MessagesState(TypedDict):
    # 对话的数据类型：用户消息+模型回复+工具+提示词
    messages: Annotated[list[BaseMessage], add_messages]


# 定义模型节点
async def llm_call(state: MessagesState, prompt: str, tool_info: ToolInfo):
    """LLM decides whether to call a tool or not"""
    llm_with_tools = tool_info["llm_with_tools"]
    messages = [
                   SystemMessage(
                       content=prompt
                   )
               ] + state["messages"]

    response = await llm_with_tools.ainvoke(messages)
    return {'messages': [response]}


# 定义工具节点
async def tool_node(state: MessagesState, tool_info: ToolInfo):
    """Performs the tool call"""

    tools_by_name = tool_info["tools_by_name"]
    # 取对话里的最后一条
    last_message = state["messages"][-1]
    task = [
        tools_by_name[tool_call["name"]].ainvoke(tool_call['args']) for tool_call in last_message.tool_calls
    ]
    # 并发执行所有工具
    observations = await asyncio.gather(*task)
    tool_messages = [
        ToolMessage(content=observation, tool_call_id=tool_call["id"])
        for observation, tool_call in zip(observations, last_message.tool_calls)
    ]
    return {'messages': tool_messages}


# 定义结束逻辑
def should_continue(state: MessagesState):
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we stop (reply to the user)
    return END


# 构建并编译agent，构建执行顺序
def build_state_graph(checkpointer: AsyncPostgresSaver, store: AsyncPostgresStore, prompt: str,
                      tool_info: ToolInfo):
    # Build workflow
    agent_builder = StateGraph(MessagesState)  # type: ignore
    # Add nodes
    agent_builder.add_node("llm_call", partial(llm_call, prompt=prompt, tool_info=tool_info))  # type: ignore
    agent_builder.add_node("tool_node", partial(tool_node, tool_info=tool_info))  # type: ignore
    # Add edges to connect nodes
    agent_builder.add_edge(START, "llm_call")
    agent_builder.add_edge(START, "llm_call")
    agent_builder.add_conditional_edges(
        "llm_call",
        should_continue,
        ["tool_node", END]
    )

    agent_builder.add_edge("tool_node", "llm_call")

    # Compile the agent
    agent = agent_builder.compile(checkpointer=checkpointer,
                                  store=store,
                                  )
    return agent


# 获取全局缓存的工具数据(websocket专用)
def get_tool_list_ws(websocket: WebSocket) -> ToolInfo:
    tool_info = getattr(websocket.app.state, 'tool_cache', None)
    if tool_info is None:
        raise RuntimeError('工具数据未找到')
    return tool_info


# 获取全局缓存的工具数据(http专用)
def get_tool_list_http(request: Request) -> ToolInfo:
    tool_info = getattr(request.app.state, 'tool_cache', None)
    if tool_info is None:
        raise RuntimeError('工具数据未找到')
    return tool_info
