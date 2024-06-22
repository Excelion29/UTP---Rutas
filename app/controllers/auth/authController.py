
from app.response.APIResponse import APIResponse
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from database.models.users import UserDB

from app.utils.security import create_access_token,create_refresh_token,verify_password,decode_token

from app.validate.auth.validateRegister import validate_new_user
from app.service.authService import register
from app.schemas.UserSchema import UserResource

async def register_user(user, db):
    try:
        validate_user = await validate_new_user(user, db)
        service = await register(validate_user, db)
        resource = UserResource.from_orm(service)

        return APIResponse.success(resource.dict(), "Usuario registrado exitosamente", status.HTTP_201_CREATED)
    except HTTPException as e:
        return APIResponse.fail(str(e.detail), status_code=e.status_code)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username or email already exists")
    except Exception as e:
        db.rollback()
        return APIResponse.fail(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
async def login_user(user, db):
    existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if not existing_user or not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",headers={"WWW-Authenticate": "Bearer"})
    
    # Crear el access token y obtener su fecha de expiración
    access_token = create_access_token(data=existing_user, db=db)
    
    return {
        "access_token": access_token.token,
        "token_type": "Bearer",
        "name": existing_user.name,
        "email": existing_user.email,
        "expire": access_token.expires_at,
    }

async def get_user(access_token,db):
    access_token = decode_token(access_token,db)
    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = access_token.user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token data", headers={"www-Authenticate":"Bearer"})
    
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "name": user.name,
            "email": user.email
        }
    )
    
async def refresh_token_user(access_token,db):
    access_token = decode_token(access_token,db)
    
    refresh_token = create_refresh_token(access_token=access_token, db=db)
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content = {
            "message": "Authorized",
            "details": {
                "access_token": refresh_token.token,
                "token_type": "Bearer",
                "name": access_token.user.name,
                "email": access_token.user.email,
                "expire": refresh_token.expires_at,
            }
        }
    )

    