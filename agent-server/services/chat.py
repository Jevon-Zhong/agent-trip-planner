import asyncio
import json
import os
from typing import Dict, Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_classic.chains.question_answering.map_reduce_prompt import messages
from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk, ToolMessage
from sqlmodel import Session, select, delete, and_

from model_prompt import prompt, map_prompt, question_prompt
from models.conversations_list import ConversationsList
from state_graph import ToolInfo, build_state_graph, tongyi_position
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


async def main_model(thread_id: str, openid: str, content: str, session: Session, tool_info: ToolInfo):
    print('main_model')
    # 存储会话
    await storage_conversation(thread_id, openid, content, session)
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
                "thread_id": thread_id,
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


# 存储会话
async def storage_conversation(thread_id: str, openid: str, content: str, session: Session):
    # 查询会话是否存在
    get_conversations_list_statement = select(ConversationsList).where(
        ConversationsList.openid == openid,
        ConversationsList.thread_id == thread_id
    )
    conversations_list = session.exec(get_conversations_list_statement).first()  # type: ignore
    # 没有就创建
    if not conversations_list:
        conversations_storage = ConversationsList(openid=openid, thread_id=thread_id, title=content)
        session.add(conversations_storage)
        session.commit()


async def delete_conversation_from_list(
        thread_id: str,
        openid: str,
        session: Session
) -> Dict[str, Any]:
    """
    从 ConversationsList 表中删除指定 thread_id + openid 对应的会话记录
    :param thread_id: 要删除的会话ID
    :param openid: 用户唯一标识（和存储逻辑对齐，避免误删）
    :param session: SQLAlchemy 的 Session 实例
    :return: 删除结果（是否成功、影响行数）
    """
    # 1. 入参校验
    if not thread_id or not openid:
        return {
            "success": False,
            "message": "thread_id 和 openid 不能为空",
            "affected_rows": 0
        }

    try:
        # 2. 先查询确认记录存在（可选，便于返回更精准的提示）
        get_statement = select(ConversationsList).where(
            ConversationsList.openid == openid,
            ConversationsList.thread_id == thread_id
        )
        existing_record = session.exec(get_statement).first()  # type: ignore
        if not existing_record:
            print(f"ConversationsList 中无 thread_id={thread_id} + openid={openid} 的记录，无需删除")
            return {
                "msg": f"ConversationsList 中无 thread_id={thread_id} + openid={openid} 的记录，无需删除",
            }

        # 3. 执行删除操作（使用 delete 语句，精准匹配）
        delete_statement = delete(ConversationsList).where(
            and_(ConversationsList.openid == openid,
                 ConversationsList.thread_id == thread_id
                 )
        )
        # 执行删除并获取影响的行数
        result = session.exec(delete_statement)
        # 提交事务（和你存储会话的 commit 逻辑一致）
        session.commit()

        affected_rows = result.rowcount
        print(f"成功删除 ConversationsList 中 thread_id={thread_id} 的记录，影响行数：{affected_rows}")
        return {
            "msg": f"成功删除 ConversationsList 中 thread_id={thread_id} 的记录，影响行数：{affected_rows}",
            "data": affected_rows
        }

    except Exception as e:
        # 异常时回滚事务，避免数据不一致
        session.rollback()
        print(f"删除 ConversationsList 记录失败：{str(e)}")
        return {
            "msg": f"删除 ConversationsList 记录失败：{str(e)}",
            "data": 0
        }


# 获取某个会话下的对话记录数据
async def conversation_detail(thread_id: str, tool_info: ToolInfo):
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
                "thread_id": thread_id,
            }
        }
        # 存储对话历史
        history = []
        # 请求历史对话数据
        async for snap in graph.aget_state_history(config):
            # print(snap, '+' * 50)
            history.append(snap)
        if not history:
            return []
        # 获取message里的内容
        valid_snaps = [snap for snap in history if snap.values.get('messages')]
        if not valid_snaps:
            return []
        # 排序，把最近的对话取到后面展示,step数越大即为最近的对话记录，无对话记录就取-1
        latest_snap = max(valid_snaps, key=lambda s: s.metadata.get("step", -1))
        msgs = latest_snap.values.get("messages")
        # 构建返回格式，返回给前端
        formatted = []
        for item in msgs:
            if isinstance(item, HumanMessage):
                formatted.append({"role": "user", "content": item.content})
            elif isinstance(item, AIMessage):
                if item.content:
                    formatted.append({"role": "assistant", "content": item.content})
                if getattr(item, "tool_calls", None):
                    for call in item.tool_calls:
                        tool_name = call["name"]
                        formatted.append({"role": "tool", "content": tool_name})
            # 获取工具结果
            elif isinstance(item, ToolMessage):
                formatted.append({"role": "tool_result", "content": {item.name: item.content}})
        return formatted


# 删除某条对话记录
async def delete_conversation_by_thread_id(thread_id: str, session: Session, openid: str, tool_info: ToolInfo):
    """
    删除指定 thread_id 对应的所有对话数据（checkpoint + 关联存储数据）
    :param thread_id: 要删除的会话ID
    :param tool_info: 工具信息（和你原代码保持一致的入参）
    :return: dict - 删除结果（是否成功、删除的checkpoint数量）
    """
    if not thread_id:
        return {
            "data": [],
            "code": 404,
            "msg": 'thread_id 不能为空'
        }

    try:
        # 复用你原代码的数据库连接方式
        async with (
            AsyncPostgresStore.from_conn_string(DB_URI) as store,
            AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer,
        ):
            await store.setup()
            await checkpointer.setup()

            # 核心：调用官方 delete_thread 方法删除该 thread_id 的所有 checkpoint
            # 该方法会自动筛选并删除该 thread_id 下的所有 checkpoint 数据
            await checkpointer.adelete_thread(thread_id)

            # 步骤2：删除 ConversationsList 中的记录（即使checkpoint删失败，也可按需调整逻辑）
            await delete_conversation_from_list(thread_id, openid, session)

            # （可选）验证删除结果：查询该 thread_id 是否还有数据
            config = {
                "configurable": {
                    "thread_id": thread_id,
                }
            }
            # 构建图（用于验证）
            graph = build_state_graph(checkpointer, store, prompt, tool_info)
            # 检查是否还有剩余的状态快照
            remaining_snaps = []
            async for snap in graph.aget_state_history(config):
                remaining_snaps.append(snap)

            deleted_count = len(remaining_snaps) == 0
            return {
                "data": [],
                "msg": f"thread_id={thread_id} 的对话数据已成功删除"
            }

    except Exception as e:
        # 捕获并返回异常信息，方便排查问题
        return {
            "data": [],
            "code": 500,
            "msg": f"删除失败：{str(e)}"
        }


# 获取经纬度数据
async def location_data(content: str, tool_info: ToolInfo):
    print("进入")
    try:
        agent = create_agent(
            model=tongyi_position,
            system_prompt=map_prompt,
            tools=tool_info["all_tools"]
        )
        res = await agent.ainvoke(
            {"messages": [{"role": "user", "content": content}]}  # type: ignore
        )
        print(res)
        ai_msg = next(
            (m for m in reversed(res["messages"]) if isinstance(m, AIMessage)),
            None
        )
        print(ai_msg)
        if ai_msg:
            data = json.loads(ai_msg.content)
            print(data)
            return data
        else:
            return []
    except Exception as e:
        print(e)
        return []

# 获取快捷提问数据
async def quick_question(content: str):
    try:
        agent = create_agent(
            model=tongyi_position,
            system_prompt=question_prompt
        )
        res = await agent.ainvoke(
            {"messages": [{"role": "user", "content": content}]}  # type: ignore
        )
        print(res)
        ai_msg = next(
            (m for m in reversed(res["messages"]) if isinstance(m, AIMessage)),
            None
        )
        print(ai_msg)
        if ai_msg:
            data = json.loads(ai_msg.content)
            print(data)
            return data
        else:
            return []
    except Exception as e:
        print(e)
        return []
