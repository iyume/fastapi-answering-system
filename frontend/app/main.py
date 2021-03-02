import os
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse

from .routers.tiku.router import tiku_router
from .routers.auth import login, register
from .config import static_router

app = FastAPI(docs_url=None, redoc_url=None, openapi=None, openapi_url=None)

app.mount('/static', static_router, name='static')
app.include_router(tiku_router)
app.include_router(login.router)
app.include_router(register.router)

@app.get('/')
async def index(request: Request):
    return RedirectResponse(request.url_for('tiku_area_index'))

# Routers naming
"""
fb: fund_basis
fr: fund_regulations
sr: security_regulations
"""
