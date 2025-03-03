import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    DATABASE_URL = os.getenv('DATABASE_URL')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
    
    LOG_FORMAT = "{time} - {name} - {level} - {message}"
    LOG_DIR = "logs"
