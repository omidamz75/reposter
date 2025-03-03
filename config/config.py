import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Create base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    DATABASE_URL = f"sqlite:///{DATA_DIR}/db.sqlite3"
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
    
    LOG_FORMAT = "{time} - {name} - {level} - {message}"
    LOG_DIR = str(DATA_DIR / "logs")
