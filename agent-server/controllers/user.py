from fastapi import APIRouter
from core.response import response
from schemas.user import LoginParams
router = APIRouter(prefix="/user", tags=["用户相关接口"])


# 用户登陆接口
@router.post("/login")
async def login(req: LoginParams):
    print('用户登陆')
    print(req.code)
    return response([1, 2])
