import sys
from pathlib import Path
from loguru import logger
from config import Config

def setup_logging(name: str = None):
    """Setup logging configuration
    Args:
        name: Optional module name for specific loggers
    """
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
    
    # Add file logger with module name if provided
    log_file = f"{Config.LOG_DIR}/{'module.' + name if name else 'bot'}.log"
    logger.add(
        log_file,
        format=Config.LOG_FORMAT,
        level=Config.LOG_LEVEL,
        rotation="1 day",
        compression="zip"
    )

    return logger
