import uuid

from fastapi import APIRouter, WebSocket, Depends
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select, desc
from starlette.websockets import WebSocketDisconnect

from core.response import response
from database import get_session
from jwt import decode_token_ws, decode_jwt
from models.conversations_list import ConversationsList
from schemas.chat import ConversationsDataParams, LocationDataParams
from services.chat import main_model, conversation_detail, location_data, delete_conversation_by_thread_id
from state_graph import ToolInfo, get_tool_list_ws, get_tool_list_http

router = APIRouter(prefix="/chat", tags=["和大模型对话"])


# 和模型对话（使用普通流失输出，在小程序会中断，所以使用websocket方式）
@router.websocket('/send_message')
async def send_message(websocket: WebSocket, session: Session = Depends(get_session),
                       tool_info: ToolInfo = Depends(get_tool_list_ws)):
    # websocket 建立连接
    await websocket.accept()
    print('websocket')
    openid = await decode_token_ws(websocket)
    if openid == '401':
        return
    """ 
    前端数据格式
    {"sessionId":"xxx","content":"你好呀！"}
    """
    try:
        while True:
            data = await websocket.receive_json()
            print('收到消息:', data)
            # 参数校验
            session_id = data['sessionId'].strip()
            content = data['content'].strip()
            if not session_id or not content:
                await websocket.send_json({'role': 'end', 'content': 'sessionId和content必填！', 'code': 422})
                continue
            # await main_model(session_id, openid, content, session, tool_info)
            try:
                async for event in main_model(session_id, openid, content, session, tool_info):
                    # socket 吐出大模型返回的消息
                    await websocket.send_json(event)
                # 大模型回复结束
                await websocket.send_json({
                    "role": "end", "content": "大模型回复结束", "code": 200
                })
            except Exception as err:
                print(err)
                await websocket.send_json(
                    {"role": "end", "content": str(err), "code": 500}
                )
    except WebSocketDisconnect as error:
        print('用户断开连接', error)

# 创建会话id
@router.get('/create_conversation')
async def create_conversation(openid:str=Depends(decode_jwt)):
    session_id = str(uuid.uuid4())
    return response({'sessionId': session_id})

# 获取全部会话列表
@router.get('/all_conversation_list')
async def all_conversation_list(session: Session = Depends(get_session), openid:str=Depends(decode_jwt)):
    statement = select(ConversationsList).where(ConversationsList.openid == openid).order_by(desc(ConversationsList.created_at))
    res = session.exec(statement).all() # type: ignore
    return response(jsonable_encoder(res))

#获取某个会话下的对话记录数据
@router.get('/get_conversation_detail/{session_id}')
async def get_conversation_detail(session_id:str, openid:str=Depends(decode_jwt), tool_info:ToolInfo = Depends(get_tool_list_http)):
    res = await conversation_detail(session_id, tool_info)
    return response(res)


#删除某个会话下的对话记录数据
@router.delete('/delete_conversation/{session_id}')
async def delete_conversation(session_id:str, session: Session = Depends(get_session), openid:str=Depends(decode_jwt), tool_info:ToolInfo = Depends(get_tool_list_http)):
    res = await delete_conversation_by_thread_id(session_id,session, openid, tool_info)
    return response(res)

"""
用户： 帮我规划一个西安三日游

模型：以下是我为你规划的一个西安三日游：
第一天：秦始皇陵
第二天：华清宫
第三天：武则天乾陵
"""

# 获取经纬度数据
@router.post('/get_location_data')
async def get_location_data(req:LocationDataParams, openid:str=Depends(decode_jwt), tool_info:ToolInfo = Depends(get_tool_list_http)):
    print(req.content)
    res = await location_data(req.content, tool_info)
    return response(res)

