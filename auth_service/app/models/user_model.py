from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    phone = Column(String(10), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_verified = Column(Integer, default=0)
    is_active = Column(Integer, default=1)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), onupdate=text('now()'), nullable=False)

    def __repr__(self):
        return f"<User(username={self.username}, phone={self.phone}, is_verified={self.is_verified})>"
