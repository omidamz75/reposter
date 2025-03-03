from telegram.ext import Application, CommandHandler
from config import Config
from core.logger import setup_logging

# Setup logging
logger = setup_logging()

async def start_handler(update, context):
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"سلام {user_name}! به ربات ریپوستر خوش آمدید.")

def main():
    try:
        logger.info("Starting bot...")
        
        # Create application
        application = Application.builder().token(Config.BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_handler))
        
        # Log successful initialization
        logger.info("Bot initialized successfully!")
        
        # Start bot
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
        raise

if __name__ == '__main__':
    main()
