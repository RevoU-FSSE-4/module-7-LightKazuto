from model.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func


class Review(Base):
    __tablename__ = "user_review"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    users_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    email = mapped_column(String(100), nullable=True)
    rating = mapped_column(Integer)
    review_content = mapped_column(Text)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Review {self.id}>"
