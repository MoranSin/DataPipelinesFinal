from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

db_username = "user"
db_password = "password"
db_name = "music_charts"
db_host = "postgres"
db_port = 5432

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except OperationalError as e:
    print(f"Error connecting to the database: {e}")

def get_db():
    """Yield a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db():
    """Create database tables based on Base metadata."""
    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError:
        pass

def test_connection():
    """Test the database connection."""
    try:
        engine.connect()
        print("Connection established")
    except OperationalError:
        print("Connection failed")