from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import PlainTextResponse, RedirectResponse

from .routers.tiku.router import tiku_router
from .routers.auth import login, register
from .config import static_router


app = FastAPI(redoc_url=None, openapi=None)

app.mount('/static', static_router, name='static')
app.include_router(tiku_router)
app.include_router(login.router)
app.include_router(register.router)

@app.get('/')
async def index(request: Request):
    return RedirectResponse(request.url_for('tiku_area_index'))

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(getattr(exc, 'detail', 'Bad request'), status_code=400)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 404:
        return PlainTextResponse('Page not found', status_code=404)
    return PlainTextResponse(exc.detail, status_code=exc.status_code)
