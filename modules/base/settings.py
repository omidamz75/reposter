from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔔 تنظیمات اعلان‌ها", callback_data="settings_notifications")],
        [InlineKeyboardButton("🕒 تنظیمات زمانی", callback_data="settings_timezone")],
        [InlineKeyboardButton("👁 تنظیمات نمایش", callback_data="settings_display")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="menu_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⚙️ تنظیمات:", reply_markup=reply_markup)

def get_settings_handlers():
    return [CommandHandler("settings", settings_command)]
