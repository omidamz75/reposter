from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters
)
from core.logger import setup_logging
from .services import ChannelService
from ..users.services import UserService

logger = setup_logging(__name__)

# Conversation states
AWAIT_CHANNEL_FORWARD = 1

async def channel_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show channel management menu"""
    user = await UserService.get_user_by_telegram_id(update.effective_user.id)
    if not user:
        await update.message.reply_text("لطفا اول با دستور /register ثبت‌نام کنید.")
        return

    keyboard = [
        [InlineKeyboardButton("➕ افزودن کانال", callback_data="channel_add")],
        [InlineKeyboardButton("📊 لیست کانال‌ها", callback_data="channel_list")],
        [InlineKeyboardButton("✅ کانال‌های فعال", callback_data="channel_active"),
         InlineKeyboardButton("❌ کانال‌های غیرفعال", callback_data="channel_inactive")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎛 مدیریت کانال‌ها:", reply_markup=reply_markup)

async def start_add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the add channel process"""
    query = update.callback_query
    await query.answer()
    
    await query.message.edit_text(
        "لطفاً یک پیام از کانال مورد نظر فوروارد کنید."
        "\n⚠️ دقت کنید که باید ادمین کانال باشید."
    )
    return AWAIT_CHANNEL_FORWARD

async def handle_channel_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle forwarded message from channel"""
    forward = update.message.forward_from_chat
    if not forward or forward.type != 'channel':
        await update.message.reply_text("لطفاً یک پیام از کانال فوروارد کنید!")
        return AWAIT_CHANNEL_FORWARD

    # First verify ownership
    success, message, msg_id = await ChannelService.verify_ownership(
        forward.id, 
        update.effective_user.id,
        context.bot
    )
    
    if not success:
        await update.message.reply_text(message)
        return AWAIT_CHANNEL_FORWARD

    # Then add channel
    success, message = await ChannelService.add_channel(
        chat_id=forward.id,
        title=forward.title,
        username=forward.username or "",
        owner_id=update.effective_user.id
    )
    
    await update.message.reply_text(message)
    if success:
        # Clean up verification message
        try:
            await context.bot.delete_message(forward.id, msg_id)
        except:
            pass
        return ConversationHandler.END
    return AWAIT_CHANNEL_FORWARD

async def cancel_add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the add channel process"""
    await update.message.reply_text("عملیات لغو شد.")
    return ConversationHandler.END

async def handle_channel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle channel menu callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "channel_menu":
        return await channel_menu(update, context)
        
    user_id = update.effective_user.id

    if query.data == "channel_list":
        channels = await ChannelService.get_user_channels(user_id)
        text = "📊 لیست تمام کانال‌های شما:\n\n"
    elif query.data == "channel_active":
        channels = await ChannelService.get_user_channels(user_id, active_only=True)
        text = "📊 لیست کانال‌های فعال:\n\n"
    elif query.data == "channel_inactive":
        channels = await ChannelService.get_user_channels(user_id, active_only=False)
        text = "📊 لیست کانال‌های غیرفعال:\n\n"
    else:
        return

    for channel in channels:
        status = "🟢" if channel.is_active else "🔴"
        text += f"{status} {channel.title}"
        if channel.username:
            text += f" (@{channel.username})"
        text += "\n"

    keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="channel_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text(text, reply_markup=reply_markup)

async def show_channel_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show channel statistics"""
    query = update.callback_query
    await query.answer()
    
    channel_id = int(query.data.split('_')[2])
    stats = await ChannelService.get_channel_stats(channel_id)
    
    if not stats:
        await query.message.edit_text("آمار کانال یافت نشد!")
        return

    text = f"📊 آمار کانال {stats['title']}:\n\n"
    text += f"🔢 تعداد کل پست‌ها: {stats['total_posts']}\n"
    text += f"✅ پست‌های موفق: {stats['successful_posts']}\n"
    text += f"📈 نرخ موفقیت: {stats['success_rate']:.1f}%\n"
    text += f"🔐 تأیید مالکیت: {'✅' if stats['is_verified'] else '❌'}\n"
    text += f"⚡️ وضعیت: {'فعال' if stats['is_active'] else 'غیرفعال'}\n"
    
    if stats['last_post']:
        text += f"🕒 آخرین پست: {stats['last_post'].strftime('%Y-%m-%d %H:%M')}\n"

    keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="channel_menu")]]
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

def get_channel_handlers():
    """Return all handlers related to channel management"""
    # Regular handlers
    channel_handlers = [
        CommandHandler("channels", channel_menu),
        CallbackQueryHandler(show_channel_stats, pattern=r"^channel_stats_\d+$"),
        CallbackQueryHandler(handle_channel_callback, pattern=r"^channel_(?!add|stats_)\w+$")
    ]

    # Separate conversation handler for adding channels
    forward_handler = ConversationHandler(
        entry_points=[CommandHandler("add_channel", start_add_channel)],
        states={
            AWAIT_CHANNEL_FORWARD: [
                MessageHandler(filters.FORWARDED & filters.ChatType.CHANNEL, handle_channel_forward)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_add_channel)],
        name="add_channel_forward"
    )

    # Conversation handler for inline menu
    menu_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_add_channel, pattern=r"^channel_add$")],
        states={
            AWAIT_CHANNEL_FORWARD: [
                CallbackQueryHandler(channel_menu, pattern=r"^channel_menu$")
            ],
        },
        fallbacks=[CallbackQueryHandler(channel_menu, pattern=r"^channel_menu$")],
        name="add_channel_menu",
        per_message=True
    )

    channel_handlers.extend([forward_handler, menu_handler])
    return channel_handlers
