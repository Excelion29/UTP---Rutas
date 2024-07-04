
from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

class RoutesDB(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, autoincrement=True, name="routes_id")
    start_location = Column(String(255),nullable=False) 
    end_location = Column(String(255),nullable=False) 
    distance = Column(String(255),nullable=False) 
    estimated_time = Column(String(255),nullable=False) 
    
    is_enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
