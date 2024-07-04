
from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class VechiclesDB(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, autoincrement=True, name="vehicles_id")
    license_plate = Column(String(20), unique=True, nullable=True)
    transport_mode_id = Column(Integer, ForeignKey('transport_modes.tmodes_id'), nullable=False)
    
    is_enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    mode = relationship("TransportModesDB", back_populates="vehicles")