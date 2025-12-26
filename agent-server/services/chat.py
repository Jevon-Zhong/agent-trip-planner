import os

from dotenv import load_dotenv
from langchain_classic.chains.question_answering.map_reduce_prompt import messages
from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk, ToolMessage
from sqlmodel import Session

from model_prompt import prompt
from state_graph import ToolInfo, build_state_graph
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore

from tools_desc import TOOL_LIST

load_dotenv()

DB_URI = os.getenv('DB_URI')

# 和模型对话
"""
thread_id: 对话id
user_id: 用户id, openid
content: 用户的问题
tool_info: 工具数据
"""


async def main_model(session_id: str, openid: str, content: str, session: Session, tool_info: ToolInfo):
    print('main_model')
    # 数据库连接、建表
    async with (
        AsyncPostgresStore.from_conn_string(DB_URI) as store,
        AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer,
    ):
        await store.setup()
        await checkpointer.setup()
        # 连接 state_graph
        graph = build_state_graph(checkpointer, store, prompt, tool_info)
        # 会话id配置
        config = {
            "configurable": {
                "thread_id": session_id,
                "user_id": openid,
            }
        }
        # 开始流式输出
        async for chunk, metadata in graph.astream(
                {"messages": [{"role": "user", "content": content}]},
                config=config,
                stream_mode="messages",
        ):
            print(chunk, '+' * 50)
            # chunk["messages"][-1].pretty_print()
            # 匹配查找工具调用
            if isinstance(chunk, AIMessageChunk) and chunk.tool_calls:
                for item in chunk.tool_calls:
                    # 工具名称
                    tool_name = item["name"]
                    # 对象key匹配对应的名称
                    desc = TOOL_LIST.get(tool_name, "未知工具")
                    if desc == "未知工具":
                        continue
                    # 整体数据格式返回给前端
                    yield {"role": "tool", "content": desc}

            # 匹配工具调用结果
            elif isinstance(chunk, ToolMessage):
                yield {"role": "tool_result", "content": {chunk.name: chunk.content}}

            # 模型回复
            elif isinstance(chunk, AIMessageChunk) and chunk.content:
                # print(chunk.content + "----------------------")
                yield {"role": "assistant", "content": chunk.content}