import asyncio
import os

from dotenv import load_dotenv
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langgraph.graph import add_messages, StateGraph, START, END

from tools import client
from langchain_community.chat_models.tongyi import ChatTongyi
from typing_extensions import TypedDict, Annotated

load_dotenv()

# 读取环境变量
API_KEY = os.getenv("API_KEY")

# 模型参数传递
tongyi = ChatTongyi(
    model='qwen3-max',
    api_key=API_KEY,
)


# 工具类型
class ToolInfo(TypedDict):
    tools_by_name: dict[str, BaseTool]
    llm_with_tools: Runnable[LanguageModelInput, BaseMessage]


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
        tools_by_name[tool_call["name"]].ainvoke(tool_call['args']) for tool_call in last_message["tool_calls"]
    ]
    # 并发执行所有工具
    observations = await asyncio.gather(*task)
    tool_messages = [
        ToolMessage(content=observation, tool_call_id=tool_call["id"])
        for observation, tool_call in zip(observations, last_message["tool_calls"])
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
    return 'end'

# 构建并编译agent，构建执行顺序
def state_graph():
    # Build workflow
    agent_builder = StateGraph(MessagesState) # type: ignore
    # Add nodes
    agent_builder.add_node("llm_call", llm_call) # type: ignore
    agent_builder.add_node("tool_node", tool_node) # type: ignore
    # Add edges to connect nodes
    agent_builder.add_edge(START, "llm_call")
    agent_builder.add_conditional_edges(
        "llm_call",
        should_continue,
        ["tool_node", END]
    )

    # Compile the agent
    agent = agent_builder.compile()
    return agent