from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr
    password: str 

class Carrier(BaseModel):
    name: str
    dni: str
    password: str 
    
class UserResource(BaseModel):
    name: str
    email: str

    @staticmethod
    def from_orm(user_orm):
        return UserResource(name=user_orm.name, email=user_orm.email)
class CarrierResource(BaseModel):
    name: str
    dni: str

    @staticmethod
    def from_orm(carrier_orm):
        return CarrierResource(name=carrier_orm.name, dni=carrier_orm.dni)
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class CarrierLogin(BaseModel):
    dni: str
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
        
class CarrierLogin(BaseModel):
    dni: str
    password: str
    class Config:
        schema_extra = {
            "example": {
                "dni": "#######",
                "password": "password"
            }
        }