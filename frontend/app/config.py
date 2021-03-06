import secrets
import logging

from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.routing import Mount

try:
    import pretty_errors
except ImportError:
    ...
else:
    pretty_errors.replace_stderr()


super_secret = secrets.token_urlsafe(32)

logger = logging.getLogger('uvicorn')


templates = Jinja2Templates(directory='app/templates')

static_router = Mount('/', StaticFiles(directory='app/static'))
# first param for the subrouter, like '/css' for '/static/css'
