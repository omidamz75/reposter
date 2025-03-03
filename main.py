from telegram.ext import Application
from config import Config
from core import setup_logging
from core.database import Base, engine
from modules.base import get_base_handlers
from modules.users.handlers import get_user_handlers
from modules.channels.handlers import get_channel_handlers

# Setup database
Base.metadata.create_all(bind=engine)

# Setup logging
logger = setup_logging()

def main():
    try:
        logger.info("Starting bot...")
        
        # Create application
        application = Application.builder().token(Config.BOT_TOKEN).build()
        application.bot_data["admin_id"] = Config.ADMIN_ID
        
        # Add handlers in order of priority
        handler_groups = [
            get_base_handlers(),      # Basic commands
            get_user_handlers(),      # User management
            get_channel_handlers(),   # Channel management
        ]
        
        for handlers in handler_groups:
            for handler in handlers:
                application.add_handler(handler)
        
        logger.info("Bot initialized successfully!")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
        raise

if __name__ == '__main__': 
    main()
