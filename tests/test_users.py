import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.users.models import User
from modules.users.handlers import register_user, admin_menu
from modules.users.services import get_db_session
from core.database import Base

# Use in-memory SQLite for testing
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
def mock_db_session(monkeypatch, test_db):
    """Replace the production database session with test database"""
    def get_test_db():
        return test_db
    
    from modules.users.services import get_db_session
    monkeypatch.setattr("modules.users.services.SessionLocal", lambda: test_db)

@pytest.fixture
def mock_regular_user():
    """Create a regular (non-admin) user fixture"""
    return User(
        telegram_id=12345,
        first_name="Regular",
        username="regular_user",
        is_admin=False,
        is_active=True
    )

@pytest.mark.asyncio
async def test_register_user(mock_update, mock_context, mock_db_session, test_db):
    """Test user registration process"""
    # Ensure user doesn't exist
    assert test_db.query(User).count() == 0
    
    # First registration
    mock_update.message.reply_text.reset_mock()
    await register_user(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once_with("ثبت‌نام شما با موفقیت انجام شد!")
    
    # Verify user was created
    assert test_db.query(User).count() == 1
    
    # Try registering again
    mock_update.message.reply_text.reset_mock()
    await register_user(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once_with("شما قبلاً ثبت‌نام کرده‌اید!")
    
    # Verify no additional user was created
    assert test_db.query(User).count() == 1

@pytest.mark.asyncio
async def test_admin_menu(mock_update, mock_context, mock_db_session, test_db, mock_regular_user):
    """Test admin menu access"""
    # Create admin user
    admin = User(telegram_id=mock_update.effective_user.id, is_admin=True)
    test_db.add(admin)
    test_db.commit()
    
    # Test admin menu access
    await admin_menu(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()
    assert "پنل مدیریت" in mock_update.message.reply_text.call_args[0][0]
    
    # Test regular user access (should be denied)
    mock_update.message.reply_text.reset_mock()
    # Create new mock user with regular user's telegram_id
    update_user = User(id=mock_regular_user.telegram_id, first_name="Regular", username="regular_user")
    mock_update.effective_user = update_user
    await admin_menu(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()
    assert "دسترسی" in mock_update.message.reply_text.call_args[0][0]
