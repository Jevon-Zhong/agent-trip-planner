from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    avatar: str = Field(nullable=False)
    nickname: str = Field(nullable=False)
    openid: str = Field(nullable=False, unique=True, index=True)