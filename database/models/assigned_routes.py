
from config.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, Enum, func
from sqlalchemy.orm import relationship
from enums.StatusRoute import StatusRoute

class AssignedRoutesDB(Base):
    __tablename__ = "assigned_routes"

    id = Column(Integer, primary_key=True, autoincrement=True, name="aroutes_id")
    route_id = Column(Integer, ForeignKey('routes.routes_id'), nullable=False)
    vehicle_id = Column(Integer, ForeignKey('vehicles.vehicles_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    travel_summary_id = Column(Integer, ForeignKey('travel_summary.tsummary_id'))
    status = Column(Enum(StatusRoute), nullable=False, default=StatusRoute.pendiente) 
    
    start_at = Column(DateTime(timezone=True), nullable=True)
    end_at = Column(DateTime(timezone=True), nullable=True)
    
    is_enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    route = relationship("RoutesDB", back_populates="assigned_routes")
    vehicle = relationship("VehiclesDB", back_populates="assigned_routes")
    user = relationship("UserDB", back_populates="assigned_routes")
    
    travel_summary = relationship("TravelSummaryDB", back_populates="assigned_routes")