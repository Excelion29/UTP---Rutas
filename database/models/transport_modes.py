
from config.database import Base
from sqlalchemy import Column, Integer, Boolean, DateTime, Enum, Text, func
from enums.VehicleType import VehicleType

class TransportModesDB(Base):
    __tablename__ = "transport_modes"

    id = Column(Integer, primary_key=True, autoincrement=True, name="tmodes_id")
    name = Column(Enum(VehicleType), nullable=False) 
    description  = Column(Text(), nullable=True)
    
    is_enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
