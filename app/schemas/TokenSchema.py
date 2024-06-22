from pydantic import BaseModel
from app.schemas.UserSchema import User
    
class Token(BaseModel):
    token: str
    scopes: str
    expires_at: str
    
class TokenData(BaseModel):
    username: str | None = None
    
class UserInDB(User):
    hashed_password: str