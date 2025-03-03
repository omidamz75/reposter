import pytest
from unittest.mock import Mock, AsyncMock
from telegram import Update, User, Chat, Message
from telegram.ext import ContextTypes, Application, CallbackContext
from config import Config

@pytest.fixture
def app():
    application = Application.builder().token(Config.BOT_TOKEN).build()
    return application

@pytest.fixture
def mock_user():
    return User(id=Config.ADMIN_ID, first_name="Test", is_bot=False, username="test_user")

@pytest.fixture
def mock_chat():
    return Chat(id=Config.ADMIN_ID, type="private")

@pytest.fixture
def mock_message(mock_user, mock_chat):
    """Create a mock message"""
    message = Mock()
    message.message_id = 1
    message.date = 1632152433
    message.chat = mock_chat
    message.from_user = mock_user
    message.text = "/start"
    message.reply_text = AsyncMock()
    message.edit_text = AsyncMock()
    return message

@pytest.fixture
def mock_update(mock_user, mock_chat, mock_message):
    """Create a mock update"""
    update = Mock(spec=Update)
    update.effective_user = mock_user
    update.effective_chat = mock_chat
    update.message = mock_message
    update.callback_query = None
    return update

@pytest.fixture
def mock_context(app):
    context = Mock(spec=CallbackContext)
    context.application = app
    context.bot = app.bot
    return context
