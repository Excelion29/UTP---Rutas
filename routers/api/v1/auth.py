from fastapi import APIRouter,HTTPException,Request
from fastapi.responses import JSONResponse
from app.schemas.UserSchema import User,UserLogin
from app.schemas.TokenSchema import Token
from fastapi import Depends,status
from config.database import get_db
from sqlalchemy.orm import Session
from app.controllers.auth.authController import register_user,login_user,get_user,refresh_token_user
from fastapi.security import OAuth2PasswordRequestForm,HTTPBearer
from typing import Annotated

auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
bearer = HTTPBearer()

@auth_router.post("/login", response_model=Token)
async def login_route(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = UserLogin(email=form_data.email, password=form_data.password)  # Asegúrate de usar form_data.username
        response = await login_user(user, db)
        
        if response:
            request.session['user'] = {
                "email": response["email"],
                "name": response["name"],
                "access_token": response["access_token"],
                "expire": response["expire"]
            }
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED,
                content = {
                    "message": "Authorized",
                    "details": {
                        "access_token": response["access_token"],
                        "token_type": "Bearer",
                        "name":response["name"],
                        "email": response["email"],
                        "expire": response["expire"],
                        }
                }
            )
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@auth_router.post("/register")
async def register_route(user: User, db: Session = Depends(get_db)):
    return await register_user(user,db)

@auth_router.post("/token", response_model=Token)
async def token_route(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = UserLogin(email=form_data.email, password=form_data.password)
        response = await login_user(user, db)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@auth_router.get("/token/refresh")
async def refresh_token_route(access_token: str = Depends(bearer), db: Session = Depends(get_db)):
    return await refresh_token_user(access_token.credentials,db)

@auth_router.get("/user")
async def user_route(access_token: str = Depends(bearer), db: Session = Depends(get_db)):
    return await get_user(access_token.credentials,db)