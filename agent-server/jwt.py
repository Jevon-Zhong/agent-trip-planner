import os
from typing import Dict, Any

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from starlette.websockets import WebSocket

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
TOKEN_EXPIRE = float(os.getenv('TOKEN_EXPIRE'))


# 生成加密token
def encode_jwt(data:Dict[str, Any]) -> str:
    # 浅拷贝
    copy_data = data.copy()
    # 计算过期时间
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE)
    copy_data['exp'] = expire
    # 生成token
    return jwt.encode(copy_data, SECRET_KEY, algorithm=ALGORITHM)

# 解析token,获取用户openid
security = HTTPBearer()
def decode_jwt(credentials: HTTPAuthorizationCredentials=Depends(security)) -> str:
    # 获取token
    token = credentials.credentials
    print(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="token is invalid",
        )
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="token is invalid",
        )
    print(payload)
    return payload['openid']

# 解析websocket 的token
async def decode_token_ws(websocket: WebSocket):
    token = websocket.headers.get('Authorization')
    print(token)
    if not token:
        await websocket.send_json({'role':'end','content':'未登陆！','code':401})
        await websocket.close()
        return '401'
    # 取出token
    # token = token.replace('Bearer ','')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        await websocket.send_json({'role': 'end', 'content': 'token已失效或不合法！', 'code': 401})
        await websocket.close()
        return '401'
    return payload['openid']



