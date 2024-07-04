from config.database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class UserPermissionsDB(Base):
    __tablename__ = "users_permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    permissions_id = Column(Integer, ForeignKey('permissions.id'), nullable=False)
    
    user = relationship("UserDB", back_populates="assigned_routes")
    permission = relationship("PermissionsDB", back_populates="assigned_routes")
