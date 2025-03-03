import os
from core.logger import setup_logging
from config import Config

def test_logger_initialization():
    """Test logger setup and file creation"""
    logger = setup_logging()
    assert os.path.exists(Config.LOG_DIR)
    
    logger.info("Test log message")
    log_file = f"{Config.LOG_DIR}/bot.log"
    assert os.path.exists(log_file)
    
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "Test log message" in content
