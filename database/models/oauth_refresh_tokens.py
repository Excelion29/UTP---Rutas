from config.database import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean

class RefreshTokenDB(Base):
    __tablename__ = "oauth_refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True, name="refresh_token_id")
    token  = Column(String, nullable=False)
    revoked = Column(Boolean, nullable=False, default=False)
    expires_at = Column(DateTime, nullable=False)