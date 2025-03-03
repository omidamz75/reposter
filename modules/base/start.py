from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👤 ثبت‌نام", callback_data="menu_register")],
        [InlineKeyboardButton("📺 مدیریت کانال‌ها", callback_data="menu_channels")],
        [InlineKeyboardButton("ℹ️ راهنما", callback_data="menu_help")],
        [InlineKeyboardButton("⚙️ تنظیمات", callback_data="menu_settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = f"سلام {update.effective_user.first_name}! به ربات ریپوستر خوش آمدید.\n"\
           "از منوی زیر گزینه مورد نظر خود را انتخاب کنید:"
           
    await update.message.reply_text(text, reply_markup=reply_markup)

def get_start_handlers():
    return [CommandHandler("start", start_command)]
