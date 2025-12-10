from typing import Any

from pydantic import BaseModel, field_validator

# 登陆参数
class LoginParams(BaseModel):
    code: str
    avatar: str
    nickname: str

    # 自定义参数校验
    @field_validator("code", "avatar", "nickname", mode='before')
    def check_not_empty(cls, v: Any, info: Any) -> Any:
        if not isinstance(v, str) or not v.strip():
            raise ValueError(f"{info.field_name}的值不能为空")
        return v

