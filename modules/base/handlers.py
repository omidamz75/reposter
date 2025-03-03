from telegram.ext import CallbackQueryHandler
from .start import start_command
from .help import help_command
from .settings import settings_command

async def handle_menu_callback(update, context):
    """Handle main menu callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "menu_main":
        await start_command(update, context)
    elif query.data == "menu_help":
        await help_command(update, context)
    elif query.data == "menu_settings":
        await settings_command(update, context)

def get_menu_handlers():
    """Get menu callback handlers"""
    return [
        CallbackQueryHandler(handle_menu_callback, pattern="^menu_")
    ]
