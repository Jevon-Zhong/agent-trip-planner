import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from controllers.user import router as user_router
from controllers.chat import router as chat_router
from core.middleware import global_err_middleware, validation_exception_handler
from database import init_db
from fastapi.staticfiles import StaticFiles


# 生命周期管瘤
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时
    init_db()
    print('应用启动时执行')
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
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
