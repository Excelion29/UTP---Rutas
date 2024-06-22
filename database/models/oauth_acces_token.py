from config.database import Base
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,Text,Boolean
from sqlalchemy.orm import relationship

class AccessTokenDB(Base):
    __tablename__ = "oauth_acces_token"

    id = Column(Integer, primary_key=True, autoincrement=True, name="token_id")
    token = Column(String, nullable=False)
    jti = Column(String, nullable=False)
    scopes = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    revoked = Column(Boolean, nullable=False, default=False)
    expires_at = Column(DateTime, nullable=False)
    
    user = relationship("UserDB", back_populates="access_tokens")



