from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class PermissionsDB(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255),nullable=False, name="name", unique=True)
    description = Column(String(255),nullable=False, name="description", unique=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
