import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from controllers.user import router as user_router
from core.middleware import global_err_middleware, validation_exception_handler

app = FastAPI()

# 全局异常处理中间件注册
app.middleware('http')(global_err_middleware)

# 全局参数校验器注册
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(user_router)
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
