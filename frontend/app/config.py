from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.routing import Mount

templates = Jinja2Templates(directory='app/templates')

static_router = Mount('/', StaticFiles(directory='app/static'))
# first param for the subrouter, like '/css' for '/static/css'

