from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

db_username = user
db_password = password
db_name = mydatabase
db_host = localhost
db_port = 5432

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db():
    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError:
        pass

def test_connection():
    try:
        engine.connect()
        print("Connection established")
    except OperationalError:
        print("Connection failed")