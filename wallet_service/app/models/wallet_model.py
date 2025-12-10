from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import text
from app.core.database import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    balance = Column(Integer, default=0)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        onupdate=text("now()"),
        nullable=False,
    )

    def __repr__(self):
        return f"<Wallet(user_id={self.user_id}, balance={self.balance}, currency={self.currency})>"

