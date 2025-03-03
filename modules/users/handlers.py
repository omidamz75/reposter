from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from core.logger import setup_logging
from .services import UserService

logger = setup_logging(__name__)

def format_user_list(users, title: str) -> tuple[str, InlineKeyboardMarkup]:
    """Format user list with back button"""
    text = f"📊 {title}:\n\n"
    for u in users:
        status = "🟢" if u.is_active else "🔴"
        role = "👑" if u.is_admin else "👤"
        text += f"{status} {role} {u.first_name}"
        if u.username:
            text += f" (@{u.username})"
        text += f" - ID: {u.telegram_id}\n"
    
    keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="admin_menu")]]
    return text, InlineKeyboardMarkup(keyboard)

async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user registration"""
    user = update.effective_user
    is_admin = user.id == context.application.bot_data.get("admin_id")
    
    success, message = UserService.register_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        is_admin=is_admin
    )
    await update.message.reply_text(message)

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all users (admin only)"""
    user = UserService.get_user_by_telegram_id(update.effective_user.id)
    
    if not user or not user.is_admin:
        await update.message.reply_text("شما دسترسی به این بخش را ندارید!")
        return

    users = UserService.get_users()
    text, _ = format_user_list(users, "لیست تمام کاربران")
    await update.message.reply_text(text)

async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin management menu"""
    user = UserService.get_user_by_telegram_id(update.effective_user.id)
    
    if not user or not user.is_admin:
        await update.message.reply_text("شما دسترسی به این بخش را ندارید!")
        return

    keyboard = [
        [InlineKeyboardButton("👥 لیست کاربران", callback_data="admin_list_users")],
        [InlineKeyboardButton("✅ کاربران فعال", callback_data="admin_active_users"),
         InlineKeyboardButton("❌ کاربران غیرفعال", callback_data="admin_inactive_users")],
        [InlineKeyboardButton("👑 لیست ادمین‌ها", callback_data="admin_list_admins")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎛 پنل مدیریت کاربران:", reply_markup=reply_markup)

async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin menu callbacks"""
    query = update.callback_query
    await query.answer()
    
    user = UserService.get_user_by_telegram_id(update.effective_user.id)
    if not user or not user.is_admin:
        await query.message.edit_text("شما دسترسی به این بخش را ندارید!")
        return

    if query.data == "admin_menu":
        keyboard = [
            [InlineKeyboardButton("👥 لیست کاربران", callback_data="admin_list_users")],
            [InlineKeyboardButton("✅ کاربران فعال", callback_data="admin_active_users"),
             InlineKeyboardButton("❌ کاربران غیرفعال", callback_data="admin_inactive_users")],
            [InlineKeyboardButton("👑 لیست ادمین‌ها", callback_data="admin_list_admins")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("🎛 پنل مدیریت کاربران:", reply_markup=reply_markup)
        return

    # Handle other callbacks
    if query.data == "admin_list_users":
        users = UserService.get_users()
        text, reply_markup = format_user_list(users, "لیست تمام کاربران")
    elif query.data == "admin_active_users":
        users = UserService.get_users(is_active=True)
        text, reply_markup = format_user_list(users, "لیست کاربران فعال")
    elif query.data == "admin_inactive_users":
        users = UserService.get_users(is_active=False)
        text, reply_markup = format_user_list(users, "لیست کاربران غیرفعال")
    elif query.data == "admin_list_admins":
        users = UserService.get_users(is_admin=True)
        text, reply_markup = format_user_list(users, "لیست ادمین‌ها")
    else:
        return

    await query.message.edit_text(text, reply_markup=reply_markup)

def get_user_handlers():
    """Return all handlers related to user management"""
    return [
        CommandHandler("register", register_user),
        CommandHandler("users", list_users),
        CommandHandler("admin", admin_menu),
        CallbackQueryHandler(handle_admin_callback, pattern="^admin_")
    ]
