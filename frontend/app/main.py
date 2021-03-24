from typing import Any

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import PlainTextResponse, RedirectResponse

from .routers import tiku, auth, user, exam, manager
from .config import static_router, templates


app = FastAPI(doc_url=None, docs_url=None, redoc_url=None, openapi=None, openapi_url=None)

app.mount('/static', static_router, name='static')
app.include_router(tiku.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(exam.router)
app.include_router(manager.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: Any) -> Any:
    return PlainTextResponse(getattr(exc, 'detail', 'Bad request'), status_code=400)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: Any
) -> Any:
    if exc.status_code == 404:
        return PlainTextResponse(exc.detail or 'Page not found', status_code=404)
    if exc.status_code == 500:
        return PlainTextResponse(exc.detail or '500 Server error', status_code=500)
    return templates.TemplateResponse(
        'base.jinja2', {
            'request': request,
            'message': exc.detail,
            'is_error_page': True
        }
    )


@app.get('/')
async def index(request: Request) -> Any:
    return RedirectResponse(request.url_for('tiku_area_index'))

@app.post('/')
async def index_post(request: Request) -> Any:
    return RedirectResponse(request.url_for('tiku_area_index'))
