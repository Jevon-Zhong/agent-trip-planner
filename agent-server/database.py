# 连接数据库
import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

# 读取环境变量
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 连接地址
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 连接引擎
engine = create_engine(DATABASE_URL)

# 会话工厂
def get_session():
    with Session(engine) as session:
        yield session

# 初始化数据库
def init_db():
    SQLModel.metadata.create_all(engine)