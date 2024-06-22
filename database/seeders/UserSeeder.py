from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas.UserSchema import User, UserResource
from database.models.users import UserDB  # Assuming User model is in models.py
from app.utils.security import hash_password
from config.database import get_db
from sqlalchemy.orm import Session

async def register_user(user: User, db: Session = Depends(get_db)):

    existing_user = db.query(UserDB).filter(
        UserDB.name == user.name or UserDB.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )

    hashed_password = hash_password(user.password)
    new_user = UserDB(name=user.name, email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()

    user_public = UserResource(name=user.name, email=user.email)  # Consider omitting email

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Usuario registrado exitosamente", "data": user_public.dict()},
    )