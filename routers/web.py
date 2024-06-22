
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi import APIRouter, Request,Depends
from fastapi.templating import Jinja2Templates
from functools import wraps

web_router = APIRouter(prefix="", tags=["root"])

templates = Jinja2Templates(directory="resources/views")

def get_current_user(f):
    @wraps(f)
    async def wrapper(request: Request, *args, **kwargs):
        user = request.session.get('user')
        # Obtener la ruta actual solicitada por el usuario
        current_route = request.url.path
        if current_route == "/login":
            # Si la ruta solicitada es /login y el usuario ya está autenticado, redirigir a dashboard
            if user:
                return RedirectResponse(url="/dashboard")
        else:
            # Para cualquier otra ruta, si no hay usuario en la sesión, redirigir a login
            if not user:
                return RedirectResponse(url="/login")
        return await f(request, *args, **kwargs)
    return wrapper

@web_router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})

@web_router.get("/login", response_class=HTMLResponse)
@get_current_user
async def root(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@web_router.get("/dashboard", response_class=HTMLResponse)
@get_current_user
async def dashboard(request: Request):
        return templates.TemplateResponse("admin/dashboard.html", {"request": request})
