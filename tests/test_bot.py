import pytest
from main import start_handler

@pytest.mark.asyncio
async def test_start_command(mock_update, mock_context):
    """Test the start command response"""
    # Call handler
    await start_handler(mock_update, mock_context)
    
    # Verify reply was called
    mock_update.message.reply_text.assert_called_once()
    args = mock_update.message.reply_text.call_args[0][0]
    assert "سلام" in args
    assert "Test" in args

def test_bot_token():
    """Test bot token format"""
    from config import Config
    assert Config.BOT_TOKEN.count(":") == 1
    assert len(Config.BOT_TOKEN.split(":")[0]) > 0
    assert len(Config.BOT_TOKEN.split(":")[1]) > 0

def test_admin_id():
    """Test admin ID configuration"""
    from config import Config
    assert isinstance(Config.ADMIN_ID, int)
    assert Config.ADMIN_ID > 0
