from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True, nullable=False)
    title = Column(String, nullable=False)
    username = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_message_id = Column(Integer, nullable=True)
    total_posts = Column(Integer, default=0)
    successful_posts = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_post_at = Column(DateTime(timezone=True), nullable=True)

    # Relationship with User model
    owner = relationship("User", backref="channels")

    @property
    def success_rate(self):
        """Calculate success rate of posts"""
        if self.total_posts == 0:
            return 0
        return (self.successful_posts / self.total_posts) * 100
