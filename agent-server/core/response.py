# 统一接口返回数据类型、格式
from typing import Any
from pydantic import BaseModel
from fastapi.responses import JSONResponse


class ResponseModel(BaseModel):
    code: int = 200
    msg: Any = "SUCCESS"
    data: Any = None


def response(
        data: Any = None,
        code: int = 200,
        msg: Any = 'SUCCESS'
) -> JSONResponse:
    if data is None:
        data = {}
    payload = ResponseModel(data=data, code=code, msg=msg).model_dump()
    return JSONResponse(content=payload, status_code=code)
