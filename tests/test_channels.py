import pytest
from unittest.mock import Mock, AsyncMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.channels.models import Channel
from modules.channels.handlers import channel_menu, handle_channel_forward
from modules.channels.services import ChannelService
from core.database import Base

# تنظیمات دیتابیس تست
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def test_db():
    """Create a fresh database for each test"""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)

@pytest.fixture
def mock_channel():
    """Create a mock channel"""
    return Channel(
        chat_id=-1001234567890,
        title="Test Channel",
        username="test_channel",
        owner_id=12345,
        is_active=True,
        is_verified=True
    )

@pytest.fixture
def mock_user_service(monkeypatch):
    """Mock UserService methods"""
    async def mock_get_user(telegram_id: int):  # اضافه کردن پارامتر
        return Mock(
            id=1, 
            telegram_id=telegram_id,
            is_admin=True, 
            is_active=True,
            first_name="Test User"
        )
    
    monkeypatch.setattr(
        "modules.channels.handlers.UserService.get_user_by_telegram_id",
        mock_get_user
    )
    return mock_get_user

@pytest.fixture
def mock_channel_service(monkeypatch):
    """Mock ChannelService methods"""
    async def mock_verify_ownership(channel_id: int, owner_id: int, bot):  # اضافه کردن پارامترها
        return True, "مالکیت کانال تأیید شد!", 123

    async def mock_add_channel(chat_id: int, title: str, username: str, owner_id: int):  # اضافه کردن پارامترها
        return True, "کانال با موفقیت ثبت شد!"

    monkeypatch.setattr(
        "modules.channels.handlers.ChannelService.verify_ownership",
        mock_verify_ownership
    )
    monkeypatch.setattr(
        "modules.channels.handlers.ChannelService.add_channel",
        mock_add_channel
    )
    return (mock_verify_ownership, mock_add_channel)

@pytest.fixture
def mock_channel_stats(monkeypatch):
    """Mock channel stats methods"""
    async def mock_update_stats(*args, **kwargs):
        return None

    async def mock_get_stats(*args, **kwargs):
        return {
            'title': "Test Channel",
            'total_posts': 3,
            'successful_posts': 2,
            'success_rate': 66.67,
            'last_post': None,
            'is_verified': True,
            'is_active': True
        }

    monkeypatch.setattr(
        "modules.channels.services.ChannelService.update_post_stats",
        mock_update_stats
    )
    monkeypatch.setattr(
        "modules.channels.services.ChannelService.get_channel_stats",
        mock_get_stats
    )
    return mock_update_stats, mock_get_stats

@pytest.mark.asyncio
async def test_channel_menu(mock_update, mock_context, mock_user_service):
    """تست منوی مدیریت کانال"""
    await channel_menu(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()
    assert "مدیریت کانال‌ها" in mock_update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_add_channel(mock_update, mock_context, mock_channel_service):
    """تست اضافه کردن کانال جدید"""
    # شبیه‌سازی پیام فوروارد شده
    mock_update.message.forward_from_chat = Mock(
        id=-1001234567890,
        title="Test Channel",
        username="test_channel",
        type="channel"
    )
    
    await handle_channel_forward(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with("کانال با موفقیت ثبت شد!")

@pytest.mark.asyncio
async def test_channel_stats(mock_update, mock_context, mock_channel_stats):
    """تست آمار کانال"""
    mock_update_stats, mock_get_stats = mock_channel_stats
    
    # تست به‌روزرسانی آمار
    await ChannelService.update_post_stats(-1001234567890, success=True)
    await ChannelService.update_post_stats(-1001234567890, success=True)
    await ChannelService.update_post_stats(-1001234567890, success=False)
    
    stats = await ChannelService.get_channel_stats(-1001234567890)
    assert stats is not None
    assert stats['total_posts'] == 3
    assert stats['successful_posts'] == 2
    assert stats['success_rate'] == pytest.approx(66.67, rel=1e-2)
