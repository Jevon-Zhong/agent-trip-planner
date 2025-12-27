from datetime import datetime
from sqlmodel import SQLModel, Field

class ConversationsList(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    openid: str = Field(index=True)
    thread_id: str = Field(index=True)
    title: str = Field()
    # 核心修改：直接生成无T的字符串时间，存入数据库
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))