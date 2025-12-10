from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import text
from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    tx_id = Column(String(50), unique=True, index=True, nullable=False)
    amount = Column(Integer, nullable=False)
    transaction_type = Column(String(10), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )

    def __repr__(self):
        return f"<Transaction(tx_id={self.tx_id}, amount={self.amount}, type={self.transaction_type}, status={self.status})>"
