from fastapi import FastAPI

from .api import api_v1 as api
from .api import auth, user

app = FastAPI(
    title='后端 API 文档',
    description='题库、用户验证功能实现',
    version='0.1.0'
)

app.include_router(api.router)
app.include_router(auth.router)
app.include_router(user.router)
