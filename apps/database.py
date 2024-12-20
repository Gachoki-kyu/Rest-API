from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings


SQLALCHEMY_DATABASE_ULR = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_ULR)

session_Local = sessionmaker(autocommit=False, autoflush=False, bind= engine)

Base = declarative_base()

def get_db():
    db = session_Local()
    try:
        yield db
    finally:
        db.close()

#try:
#    conn = psycopg2.connect(host='localhost', database = "fastAPI", user = 'postgres',
#    password ='bena313', cursor_factory = RealDictCursor)
#    cursor = conn.cursor()
#    print('Database was connected successiful')
#except Exception as error:
#    print('Failed to connect')
#    print('error :', error)
