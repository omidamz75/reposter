import sys
from pathlib import Path
from loguru import logger
from config import Config

def setup_logging():
    # Create logs directory if it doesn't exist
    Path(Config.LOG_DIR).mkdir(exist_ok=True)
    
    # Remove default logger
    logger.remove()
    
    # Add console logger
    logger.add(
        sys.stdout,
        format=Config.LOG_FORMAT,
        level=Config.LOG_LEVEL,
        colorize=True
    )
    
    # Add file logger
    logger.add(
        f"{Config.LOG_DIR}/bot.log",
        format=Config.LOG_FORMAT,
        level=Config.LOG_LEVEL,
        rotation="1 day",
        compression="zip"
    )

    return logger
