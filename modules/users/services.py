from contextlib import contextmanager
from typing import List, Optional
from core.database import SessionLocal
from core.logger import setup_logging
from .models import User

logger = setup_logging(__name__)

@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserService:
    @staticmethod
    def register_user(telegram_id: int, username: str, first_name: str, is_admin: bool = False) -> tuple[bool, str]:
        """Register a new user"""
        with get_db_session() as db:
            try:
                existing_user = db.query(User).filter(User.telegram_id == telegram_id).first()
                if existing_user:
                    return False, "شما قبلاً ثبت‌نام کرده‌اید!"

                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    is_admin=is_admin
                )
                db.add(user)
                db.commit()
                logger.info(f"New user registered: {telegram_id}")
                return True, "ثبت‌نام شما با موفقیت انجام شد!"

            except Exception as e:
                db.rollback()
                logger.error(f"Error registering user: {str(e)}")
                return False, "متأسفانه در ثبت‌نام مشکلی پیش آمد!"

    @staticmethod
    def get_user_by_telegram_id(telegram_id: int) -> Optional[User]:
        """Get user by telegram ID"""
        with get_db_session() as db:
            return db.query(User).filter(User.telegram_id == telegram_id).first()

    @staticmethod
    def get_users(is_active: Optional[bool] = None, is_admin: Optional[bool] = None) -> List[User]:
        """Get users with optional filters"""
        with get_db_session() as db:
            query = db.query(User)
            if is_active is not None:
                query = query.filter(User.is_active == is_active)
            if is_admin is not None:
                query = query.filter(User.is_admin == is_admin)
            return query.all()

    @staticmethod
    def toggle_user_status(telegram_id: int, is_active: bool) -> bool:
        """Toggle user active status"""
        with get_db_session() as db:
            try:
                user = db.query(User).filter(User.telegram_id == telegram_id).first()
                if user:
                    user.is_active = is_active
                    db.commit()
                    logger.info(f"User {telegram_id} status changed to {is_active}")
                    return True
                return False
            except Exception as e:
                db.rollback()
                logger.error(f"Error toggling user status: {str(e)}")
                return False
