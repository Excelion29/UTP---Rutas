from config.database import Base
from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, func
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, name="user_id")
    name = Column(String(255),nullable=False, name="name", unique=True)
    email = Column(EmailType,nullable=True, unique=True, name="email")
    dni = Column(String(11),nullable=True, name="dni", unique=True)
    password = Column(Text,nullable=False, name="password")
    
    access_tokens = relationship("AccessTokenDB", backref="owner")
    
    is_authorized = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
