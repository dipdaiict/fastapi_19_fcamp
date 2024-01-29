from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
print(settings.database_username)
print(settings.database_hostname)

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# SQLALCHEMY_DATABASE_URL = "postgresql://<user_name>:<password>@<ip_address>/<host_name>/<database_name>"

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Engine is Handle to connection SQLAlchemy to Connect with Database:
engine = create_engine(SQLALCHEMY_DATABASE_URL)    # connect_args={"check_same_thread": False This argument is also implement in the args but when we use SQLLite Database..

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()