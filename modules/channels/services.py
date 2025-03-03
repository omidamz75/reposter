from typing import List, Optional, Tuple
from contextlib import asynccontextmanager
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from core.database import async_engine
from core.logger import setup_logging
from .models import Channel
from telegram.error import TelegramError

logger = setup_logging(__name__)

@asynccontextmanager
async def get_db_session():
    """Async context manager for database sessions"""
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

class ChannelService:
    @staticmethod
    async def add_channel(chat_id: int, title: str, username: str, owner_id: int) -> Tuple[bool, str]:
        """Add a new channel"""
        async with get_db_session() as db:
            try:
                stmt = select(Channel).where(Channel.chat_id == chat_id)
                result = await db.execute(stmt)
                existing_channel = result.scalar_one_or_none()
                
                if existing_channel:
                    return False, "این کانال قبلاً ثبت شده است!"

                channel = Channel(
                    chat_id=chat_id,
                    title=title,
                    username=username,
                    owner_id=owner_id
                )
                db.add(channel)
                await db.commit()
                logger.info(f"New channel added: {chat_id} by user {owner_id}")
                return True, "کانال با موفقیت ثبت شد!"

            except Exception as e:
                await db.rollback()
                logger.error(f"Error adding channel: {str(e)}")
                return False, "متأسفانه در ثبت کانال مشکلی پیش آمد!"

    @staticmethod
    async def get_user_channels(owner_id: int, active_only: bool = False) -> List[Channel]:
        """Get channels owned by user"""
        async with get_db_session() as db:
            stmt = select(Channel).where(Channel.owner_id == owner_id)
            if active_only:
                stmt = stmt.where(Channel.is_active == True)
            
            result = await db.execute(stmt)
            return result.scalars().all()

    @staticmethod
    async def toggle_channel_status(chat_id: int, owner_id: int, is_active: bool) -> Tuple[bool, str]:
        """Toggle channel active status"""
        async with get_db_session() as db:
            try:
                stmt = select(Channel).where(
                    Channel.chat_id == chat_id,
                    Channel.owner_id == owner_id
                )
                result = await db.execute(stmt)
                channel = result.scalar_one_or_none()

                if not channel:
                    return False, "کانال مورد نظر یافت نشد!"

                channel.is_active = is_active
                await db.commit()
                status = "فعال" if is_active else "غیرفعال"
                logger.error(f"Channel {chat_id} status changed to {status}")
                return True, f"وضعیت کانال به {status} تغییر کرد"

            except Exception as e:
                await db.rollback()
                logger.error(f"Error toggling channel status: {str(e)}")
                return False, "متأسفانه در تغییر وضعیت کانال مشکلی پیش آمد!"

    @staticmethod
    async def verify_ownership(channel_id: int, owner_id: int, bot) -> Tuple[bool, str, Optional[int]]:
        """Verify channel ownership by checking admin rights and sending test message"""
        try:
            # Check if user is admin
            admins = await bot.get_chat_administrators(channel_id)
            is_admin = any(admin.user.id == owner_id for admin in admins)
            
            if not is_admin:
                return False, "شما ادمین این کانال نیستید!", None

            # Send verification message
            message = await bot.send_message(
                channel_id,
                "🤖 این پیام برای تأیید مالکیت کانال ارسال شده است.\n"
                "پس از تأیید، این پیام حذف خواهد شد."
            )

            async with get_db_session() as db:
                stmt = select(Channel).where(Channel.chat_id == channel_id)
                result = await db.execute(stmt)
                channel = result.scalar_one_or_none()
                if channel:
                    channel.is_verified = True
                    channel.verification_message_id = message.message_id
                    await db.commit()

            return True, "مالکیت کانال تأیید شد!", message.message_id

        except TelegramError as e:
            logger.error(f"Error verifying channel ownership: {str(e)}")
            return False, "خطا در تأیید مالکیت کانال. لطفاً دسترسی‌های ربات را بررسی کنید.", None

    @staticmethod
    async def update_post_stats(channel_id: int, success: bool = True) -> None:
        """Update channel post statistics"""
        async with get_db_session() as db:
            try:
                stmt = select(Channel).where(Channel.chat_id == channel_id)
                result = await db.execute(stmt)
                channel = result.scalar_one_or_none()
                if channel:
                    channel.total_posts += 1
                    if success:
                        channel.successful_posts += 1
                    channel.last_post_at = func.now()
                    await db.commit()
            except Exception as e:
                logger.error(f"Error updating post stats: {str(e)}")
                await db.rollback()

    @staticmethod
    async def get_channel_stats(channel_id: int) -> Optional[dict]:
        """Get channel statistics"""
        async with get_db_session() as db:
            stmt = select(Channel).where(Channel.chat_id == channel_id)
            result = await db.execute(stmt)
            channel = result.scalar_one_or_none()
            
            if not channel:
                return None

            return {
                'title': channel.title,
                'total_posts': channel.total_posts,
                'successful_posts': channel.successful_posts,
                'success_rate': channel.success_rate,
                'last_post': channel.last_post_at,
                'is_verified': channel.is_verified,
                'is_active': channel.is_active
            }
