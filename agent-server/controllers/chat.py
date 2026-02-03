import base64
import hashlib
import hmac
import os
import time
import urllib
import uuid
from urllib.parse import urlencode

from dotenv import load_dotenv
from fastapi import APIRouter, WebSocket, Depends, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select, desc
from starlette.websockets import WebSocketDisconnect

from core.response import response
from database import get_session
from jwt import decode_token_ws, decode_jwt
from models.conversations_list import ConversationsList
from schemas.chat import ConversationsDataParams, LocationDataParams
from services.chat import main_model, conversation_detail, location_data, delete_conversation_by_thread_id, \
    quick_question
from state_graph import ToolInfo, get_tool_list_ws, get_tool_list_http

router = APIRouter(prefix="/chat", tags=["和大模型对话"])

load_dotenv()
APPID = os.getenv("TENCENT_APPID")
SECRET_ID = os.getenv("TENCENT_SECRET_ID")
SECRET_KEY = os.getenv("TENCENT_SECRET_KEY")

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

# 根据用户提问记录生成用户可能会提问的快捷提问
@router.post('/get_quick_question')
async def get_quick_question(session: Session = Depends(get_session), openid:str=Depends(decode_jwt), tool_info:ToolInfo = Depends(get_tool_list_http)):
    statement = select(ConversationsList).where(ConversationsList.openid == openid).order_by(desc(ConversationsList.created_at))
    conversation_list = session.exec(statement).all()
    content_arr = []
    for conversation in conversation_list:
        content_arr.append(conversation.title)
    content:str = ','.join(content_arr)
    res = await quick_question(content)
    return response(res)

# 腾讯云 ASR 域名常量
ASR_PRE = "asr.cloud.tencent.com/asr/v2"

# 生成腾讯云WebSocket鉴权签名（关键：腾讯云要求的鉴权方式）
def generate_signature(params: dict[str, str | int | None]) -> str:
    # 1.对除 signature 之外的所有参数按字典序进行排序，拼接请求 URL （不包含协议部分：wss://）作为签名原文
    # 为什么必须排序？因为签名的生成对参数顺序敏感，如果前端 / 后端排序不一致，生成的签名就会不同，
    # 导致腾讯云接口拒绝请求（返回签名无效）。这行代码就是为了保证参数顺序的唯一性，确保签名生成正确。
    sorted_params = sorted(params.items(), key=lambda x: x[0])

    # 2. 拼接为 key1=value1&key2=value2格式
    query_str = "&".join([f"{k}={v}" for k, v in sorted_params])

    # 3. 签名原文（query_str拼接上前缀）
    signature_str = f"{ASR_PRE}/{APPID}?{query_str}"

    # 4. 对签名原文使用 SecretKey 进行 HMAC-SHA1 加密，之后再进行 base64 编码
        # 1. 将 字符串密钥 和 字符串原始数据 转换为 字节类型（必须步骤）
    secret_key_bytes = SECRET_KEY.encode('utf-8')
    raw_data_bytes = signature_str.encode('utf-8')

        # 2. 初始化 HMAC-SHA1 实例，传入密钥和哈希算法
    hmac_obj = hmac.new(
        key=secret_key_bytes,  # 密钥字节
        msg=raw_data_bytes,  # 待签名数据字节
        digestmod=hashlib.sha1  # 指定哈希算法为 SHA1
    )

        # 3. 计算 HMAC-SHA1 二进制摘要（返回 bytes 类型）
    hmac_sha1_bytes = hmac_obj.digest()

        # 4 转换为 Base64 编码字符串（接口签名最常用）
    signature_base64 = base64.b64encode(hmac_sha1_bytes).decode('utf-8')

    # 5. 将 signature 值进行 urlencode（必须进行 URL 编码，编码函数必须要支持对+、=等特殊字符的编码，否则将导致鉴权失败偶发
    return urllib.parse.quote(signature_base64)




@router.get('/get_asr_ws_url')
async def get_asr_ws_url(openid:str=Depends(decode_jwt)):
    # 定义握手所需参数
    timestamp = int(time.time())
    params = {
        "secretid": SECRET_ID, # 腾讯云注册账号的密钥 secretid，可通过 API 密钥管理页面 获取。
        "timestamp": timestamp, # 当前 UNIX 时间戳，单位为秒。如果与当前时间相差过大，会引起签名过期错误。
        "expired": timestamp + 60, # 签名的有效期截止时间 UNIX 时间戳，单位为秒。expired 必须大于 timestamp 且 expired - timestamp 小于90天。
        "nonce": int(time.time() * 1000), # 随机正整数。用户需自行生成，最长10位。示例值：8743357
        "engine_model_type": "16k_zh", # 引擎模型类型
        "voice_id": str(uuid.uuid4()), # 音频流全局唯一标识，一个 WebSocket 连接对应一个，用户自己生成（推荐使用 UUID），最长128位。
        "voice_format": 1, # 语音编码方式，可选，默认值为4。1：pcm；
        "needvad": 1 # 0：关闭 vad，1：开启 vad，默认为0。如果语音分片长度超过60秒，会强制在60s断一次，建议客户音频超过60s时，开启 vad（人声检测切分功能），提升切分效果。
    }

    # 生成 signature
    signature = generate_signature(params)

    # 拼接最终 URL
    params["signature"] = signature
    query = "&".join([f"{k}={v}" for k, v in params.items()])

    ws_url = f"wss://{ASR_PRE}/{APPID}?{query}"

    return response(ws_url)

