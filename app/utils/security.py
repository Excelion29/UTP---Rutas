from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime from datetime import datetime, timedelta
from database.models.oauth_acces_token import AccessTokenDB
from database.models.oauth_refresh_tokens import RefreshTokenDB
from fastapi import HTTPException, status, Depends
from app.schemas.TokenSchema import Token
import secrets
from fastapi import Depends
from sqlalchemy.orm import Session
from config.database import get_db
from fastapi.security import HTTPBearer

SECRET_KEY = "secret"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_DAYS = 7
REFRESH_TOKEN_EXPIRES_DAYS = 10

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_jti():
    # Generate a random, URL-safe string using secrets library (Python 3.6+)
    return secrets.token_urlsafe(32)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)

def create_access_token(data, db):
    to_encode = {"id": data.id, "name": data.name, "email" :data.email}
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    jti = create_jti()

    try:
        new_access_token = AccessTokenDB(
            token=encoded_jwt,
            jti=jti,
            scopes="Personal Access Token",
            user_id=data.id,
            expires_at=expire
        )
        db.add(new_access_token)
        db.commit()
        access_token_data = Token(token=encoded_jwt, scopes="Personal Access Token", expires_at=expire.isoformat())
        return access_token_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


def create_refresh_token(access_token, db):
    try:
        db_token = db.query(AccessTokenDB).filter_by(token=access_token.token).first()
        db_token.revoked = True
        db.commit() 
        
        new_access_token = RefreshTokenDB(
            token=access_token.token,
            expires_at=access_token.expires_at
        )
        db.add(new_access_token)
        db.commit()
        
        access_token_data = create_access_token(access_token.user,db)
        return access_token_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

def decode_token(access_token: str,db: Session = Depends(get_db)):
    try:
        db_token = db.query(AccessTokenDB).filter_by(token=access_token).first()
        
        if db_token:
            # Verificar si el token ha sido revocado
            if db_token.revoked:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has been revoked",
                )
                
            # Verificar si el token ha expirado
            if  db_token.expires_at < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                )
            # Si el token es válido y no ha sido revocado ni ha expirado, devolver los detalles del token
            
            return db_token
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token or token expired",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or token expired",
        )
    
def decode_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("token_type") == "refresh_token":
            return payload
        else:
            raise JWTError("Invalid token type")
    except JWTError:
        return None