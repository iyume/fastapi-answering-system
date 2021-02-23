import os
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse

from .routers.tiku.router import tiku_router
from .routers.login.router import login_router
from .config import static_router

app = FastAPI()

app.mount('/static', static_router, name='static')
app.include_router(tiku_router)
app.include_router(login_router)

@app.get('/')
async def index(request: Request):
    return RedirectResponse(os.path.join(str(request.base_url), '/tiku/area'))

# Routers naming
"""
fb: fund_basis
fr: fund_regulations
sr: security_regulations
"""
