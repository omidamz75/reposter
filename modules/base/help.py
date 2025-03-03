from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """🤖 راهنمای دستورات ربات:

📝 دستورات عمومی:
/start - شروع کار با ربات
/help - نمایش این راهنما
/settings - تنظیمات ربات

📺 مدیریت کانال:
/channels - مدیریت کانال‌ها
/stats - آمار کانال‌ها

👥 مدیریت کاربری:
/register - ثبت‌نام در ربات
/profile - مشاهده پروفایل"""

    keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="menu_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(help_text, reply_markup=reply_markup)

def get_help_handlers():
    return [CommandHandler("help", help_command)]
