from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config

config = Config('.env')
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

SQLALCHEMY_DATABASE_URL = f"postgresql://{config('POSTGRES_USER')}:{config('POSTGRES_PW')}@{config('POSTGRES_URL')}/{config('POSTGRES_DB')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
