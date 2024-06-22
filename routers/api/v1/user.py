from fastapi import APIRouter

user_router = APIRouter(prefix="/user")

# Rutas
@user_router.get("/all")
def root():
    return "Hi I am FastAPI"