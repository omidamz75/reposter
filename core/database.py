from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config

# Create base directories
DATABASE_URL = Config.DATABASE_URL if Config.DATABASE_URL else "sqlite:///data/bot.db"

# Create sync engine for migrations and model creation
engine = create_engine(DATABASE_URL, echo=False)

# Create async engine for operations
async_engine = create_async_engine(
    DATABASE_URL.replace('sqlite:///', 'sqlite+aiosqlite:///'),
    echo=False
)

# Create session factories
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# Create base class for models
Base = declarative_base()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
