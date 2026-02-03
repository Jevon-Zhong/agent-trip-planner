import os
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from controllers.user import router as user_router
from controllers.chat import router as chat_router
from core.middleware import global_err_middleware, validation_exception_handler
from database import init_db
from fastapi.staticfiles import StaticFiles

# 引入mcp工具
from state_graph import client, tongyi, map_data

load_dotenv()

# 读取环境变量
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

# 生命周期管瘤
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时
    init_db()
    print('应用启动时执行')
    # 读取mcp工具
    tools = await client.get_tools()
    tools += [map_data]
    # 大模型读取工具
    llm_with_tools = tongyi.bind_tools(tools)
    # 大模型绑定的工具
    tools_by_name = {tool.name: tool for tool in tools}
    # print('所有工具', tools)
    # print('大模型读取工具', llm_with_tools)
    # 全局缓存工具
    app.state.tool_cache = {'tools_by_name': tools_by_name, 'llm_with_tools': llm_with_tools, "all_tools": tools} # type: ignore
    yield
    print('应用关闭时执行')

app = FastAPI(lifespan=lifespan)

# 全局异常处理中间件注册
app.middleware('http')(global_err_middleware)

# 全局参数校验器注册
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# 存储上传图片的文件夹路径
image_folder = os.path.join(os.getcwd(), 'images')
# 开启静态资源访问
app.mount("/images", StaticFiles(directory=image_folder))
app.include_router(user_router)
app.include_router(chat_router)
if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
