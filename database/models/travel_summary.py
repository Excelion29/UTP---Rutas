
from config.database import Base
from sqlalchemy import Column, Integer, Boolean, DateTime, Text, String, Enum, func
from enums.StatusTravel import StatusTravel
from sqlalchemy.orm import relationship

class TravelSummaryDB(Base):
    __tablename__ = "travel_summary"

    id = Column(Integer, primary_key=True, autoincrement=True, name="tsummary_id")
    
    title = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    total_distance = Column(String(255),nullable=True) 
    estimated_time = Column(String(255),nullable=False) 
    
    start_at = Column(DateTime(timezone=True), nullable=False)
    end_at = Column(DateTime(timezone=True), nullable=True)
    
    status = Column(Enum(StatusTravel), nullable=False, default=StatusTravel.pendiente) 
    
    is_enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    
    assigned_routes = relationship("AssignedRoutesDB", back_populates="travel_summary")

