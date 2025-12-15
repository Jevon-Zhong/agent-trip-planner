import os
import uuid
from typing import cast

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, UploadFile
from sqlmodel import select, Session

from core.response import response
from database import get_session
from jwt import encode_jwt, decode_jwt
from models.user import User
from schemas.user import LoginParams
import httpx

load_dotenv()

# 读取环境变量
APPID = os.getenv("APPID")
SECRET = os.getenv("SECRET")

# 登陆请求地址
code2Session = 'https://api.weixin.qq.com/sns/jscode2session'

router = APIRouter(prefix="/user", tags=["用户相关接口"])


# 用户登陆接口
@router.post("/login")
async def login(req: LoginParams, session: Session = Depends(get_session)):
    print('用户登陆')
    # 构造请求参数
    params = {
        'appid': APPID,
        'secret': SECRET,
        'grant_type': 'authorization_code',
        'js_code': req.code,
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(code2Session, params=params)
        data = r.json()
        if 'errcode' in data:
            return response([], 400, data)
        openid: str = data['openid']
        # 查询用户是否已存在
        statement = select(User).where(User.openid == openid)
        # 执行sql
        userinfo = session.exec(statement).first()  # type: ignore
        print(userinfo)
        # 如果不存在这个用户
        if not userinfo:
            # 创建模型对象
            userinfo = User(
                avatar=req.avatar,
                nickname=req.nickname,
                openid=openid
            )
            # 放入会话
            session.add(userinfo)
            # 提交事物，插入到数据
            session.commit()
            # 同步数据
            session.refresh(userinfo)
        # 生成token
        token = encode_jwt({'openid': openid})
        return response({'avatar': req.avatar, 'nickname': req.nickname, 'access_token': token})


# 文件大小
MAX_FILE_SIZE = 1024 * 1024 * 10
# 文件类型
ALLOWED_CONTENT_TYPES = ['image/jpeg', 'image/png', 'image/webp']


# 图片上传（头像上传）
@router.post("/upload_image")
async def upload_image(file: UploadFile):
    print(file)
    # 图片校验
    # 校验类型
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        return response([], 422, '请上传合法头像')
    # 校验大小
    if cast(int, file.size) > MAX_FILE_SIZE:
        return response([], 422, '上传到头像太大')
    # 重命名文件
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    # 上传到服务器的文件名
    file_name = f'{uuid.uuid4()}.{file_extension}'
    # 存储上传图片的文件夹路径
    image_folder = os.path.join(os.getcwd(), 'images')
    # 文件完整路径
    file_path = os.path.join(image_folder, file_name)
    # 存入文件
    with open(file_path, 'wb') as f:
        content = await file.read()
        f.write(content)
    # 将结果返回
    return response({'upload_image_url': f"http://127.0.0.1:8000/images/{file_name}"})


# 测试解析token
@router.get("/get_openid")
async def get_openid(openid:str=Depends(decode_jwt)):
    print(openid)
