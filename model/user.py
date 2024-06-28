from model.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql import func
from flask_login import UserMixin
import bcrypt


class User(Base, UserMixin):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(50), nullable=True)
    password = mapped_column(String(255), nullable=True)
    email = mapped_column(String(100), nullable=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    role = mapped_column(String(50))

    def set_password(self, password):
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"),self.password.encode("utf-8"))

    reviews = relationship("Review", cascade="all,delete-orphan")

    def __repr__(self):
        return f'<Product {self.username}>'
