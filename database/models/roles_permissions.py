from config.database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class RolesPermissionsDB(Base):
    __tablename__ = "roles_permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    permission_id = Column(Integer, ForeignKey('permissions.id'), nullable=False)
    
    role = relationship("RolesDB", back_populates="assigned_routes")
    permission = relationship("PermissionsDB", back_populates="assigned_routes")