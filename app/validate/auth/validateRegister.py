from database.models.users import UserDB
from fastapi import HTTPException, status

async def validate_new_user(user, db):
    existing_user = db.query(UserDB).filter(
        UserDB.name == user.name or UserDB.email == user.email
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    
    return user