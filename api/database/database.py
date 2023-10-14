from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database

DATABASE_URL = "sqlite:///./test.db"  # Use your preferred database URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
database = Database(DATABASE_URL)
