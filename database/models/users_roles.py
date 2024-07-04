from config.database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class UserRolesDB(Base):
    __tablename__ = "users_roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    
    user = relationship("UserDB", back_populates="assigned_routes")
    role = relationship("RolesDB", back_populates="assigned_routes")