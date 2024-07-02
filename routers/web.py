
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
import os
from functools import wraps
from datetime import datetime

web_router = APIRouter(prefix="", tags=["root"])

templates = Jinja2Templates(directory="resources/views")

def get_current_user(f):
    @wraps(f)
    async def wrapper(request: Request, *args, **kwargs):
        user = request.session.get('user')
        current_route = request.url.path
        
        if current_route == "/login":
            # Si la ruta solicitada es /login y el usuario ya está autenticado, redirigir a dashboard
            if user:
                return RedirectResponse(url="/dashboard")
        else:
            # Para cualquier otra ruta, si no hay usuario en la sesión, redirigir a login
            if not user:
                return RedirectResponse(url="/login")
            
            # Verificar si el token de acceso ha expirado
            expire_timestamp = user.get('expire', None)
            if expire_timestamp:
                expire_datetime = datetime.strptime(expire_timestamp, "%Y-%m-%dT%H:%M:%S.%f")
                if expire_datetime < datetime.utcnow():
                    # Si el token ha expirado, limpiar la sesión y redirigir a login
                    request.session.clear()
                    return RedirectResponse(url="/login")
        
        return await f(request, *args, **kwargs)
    
    return wrapper

@web_router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    authenticated = request.session.get('user') is not None
    user_data = request.session.get('user')
    return templates.TemplateResponse("welcome.html", {"request": request, "authenticated": authenticated, "user_data": user_data})

@web_router.get("/login", response_class=HTMLResponse)
@get_current_user
async def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@web_router.get("/dashboard", response_class=HTMLResponse)
@get_current_user
async def dashboard(request: Request):
    authenticated = request.session.get('user') is not None
    user_data = request.session.get('user')
    return templates.TemplateResponse("admin/dashboard.html", {"request": request, "authenticated": authenticated, "user_data": user_data})

@web_router.get("/viajes", response_class=HTMLResponse)
@get_current_user
async def viajes(request: Request):
    authenticated = request.session.get('user') is not None
    user_data = request.session.get('user')
    return templates.TemplateResponse("admin/viajes/index.html", {"request": request, "authenticated": authenticated, "user_data": user_data})

@web_router.get("/calendario", response_class=HTMLResponse)
@get_current_user
async def calendario(request: Request):
    authenticated = request.session.get('user') is not None
    user_data = request.session.get('user')
    return templates.TemplateResponse("admin/calendario/index.html", {"request": request, "authenticated": authenticated, "user_data": user_data})

@web_router.get("/estadisticas", response_class=HTMLResponse)
@get_current_user
async def estadisticas(request: Request):
    authenticated = request.session.get('user') is not None
    user_data = request.session.get('user')
    return templates.TemplateResponse("admin/estadisticas/index.html", {"request": request, "authenticated": authenticated, "user_data": user_data})