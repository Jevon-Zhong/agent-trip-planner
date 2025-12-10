from typing import Any

from fastapi import Request
from core.response import response

# 全局异常处理中间件
async def global_err_middleware(request: Request, call_next: Any):
    try:
        # 进入下一个中间件
        return await call_next(request)
    except Exception as e:
        # 返回异常
        return response(code=500, msg=str(e))

# 全局参数异常校验函数
async def validation_exception_handler(request: Request, exc: Any):
    print('全局参数异常校验函数被触发')
    print(exc)
    first_error = exc.errors()[0]
    msg = first_error['msg']
    if msg == 'Field required':
        msg = f"缺少参数:{first_error['loc'][1]}"
    return response(code=422, msg=msg)