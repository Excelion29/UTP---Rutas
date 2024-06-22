from app.utils.security import hash_password
from database.models.users import UserDB

async def register(user, db):
    hashed_password = hash_password(user.password)
    new_user = UserDB(name=user.name, email=user.email, password=hashed_password)
    
    db.add(new_user)
    db.commit()
    
    return new_user