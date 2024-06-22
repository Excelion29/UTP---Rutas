from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr
    password: str 
    
class UserResource(BaseModel):
    name: str
    email: str

    @staticmethod
    def from_orm(user_orm):
        return UserResource(name=user_orm.name, email=user_orm.email)
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "correo@dominio.com",
                "password": "password"
            }
        }