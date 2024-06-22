from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import Settings


settings = Settings()
DB_NAME = settings.db_name
DB_USER = settings.db_user
DB_PASS = settings.db_pass
DB_HOST = settings.db_host
DB_PORT = settings.db_port


SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}, future=True
)

SessionLocal = sessionmaker(
    bind=engine,autocommit=False,autoflush=False,future=True
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()