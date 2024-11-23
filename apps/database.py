from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_ULR = 'postgresql://postgres:bena313@localhost/fastAPI'

engine = create_engine(SQLALCHEMY_DATABASE_ULR)

session_Local = sessionmaker(autocommit=False, autoflush=False, bind= engine)

Base = declarative_base()

def get_db():
    db = session_Local()
    try:
        yield db
    finally:
        db.close()