from fastapi import APIRouter, WebSocket, Depends
from starlette.websockets import WebSocketDisconnect

from jwt import decode_token_ws

router = APIRouter(prefix="/chat", tags=["和大模型对话"])


# 和模型对话（使用普通流失输出，在小程序会中断，所以使用websocket方式）
@router.websocket('/send_message')
async def send_message(websocket: WebSocket):
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
            print('收到消息:',data)
            # 参数校验
            sessionId = data['sessionId'].strip()
            content = data['content'].strip()
            if not sessionId or not content:
                await websocket.send_json({'role':'end','content':'sessionId和content必填！','code':422})
                continue
    except WebSocketDisconnect:
        print('用户断开连接')
