from config.database import Base
from sqlalchemy import Column,Integer,String,Text
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, name="user_id")
    name = Column(String(255),nullable=False, name="name", unique=True)
    email = Column(EmailType,nullable=False, unique=True, name="email")
    password = Column(Text,nullable=False, name="password")
    
    access_tokens = relationship("AccessTokenDB", backref="owner")

