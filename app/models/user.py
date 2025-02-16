from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.inventory import Inventory


class User(Base):
    """Таблица users содержит информацию о пользователях."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    coins: Mapped[int] = mapped_column(default=1000)
    transactions_sent: Mapped[List["Transaction"]] = relationship("Transaction", foreign_keys="Transaction.sender_id",
                                                                  back_populates="sender")
    transactions_received: Mapped[List["Transaction"]] = relationship("Transaction",
                                                                      foreign_keys="Transaction.receiver_id",
                                                                      back_populates="receiver")
    inventory: Mapped[List["Inventory"]] = relationship("Inventory", back_populates="user",
                                                        cascade="all, delete-orphan")

    def add_coins(self, amount: int):
        """Добавляет монеты к балансу пользователя."""
        if amount < 0:
            raise ValueError(
                "У пользователя неккоректное количество монет для добавления. Количество монет должно быть больше 0.")
        self.coins += amount

    def remove_coins(self, amount: int):
        """Удаляет монеты из баланса пользователя"""
        if self.coins < amount or self.coins - amount < 0:
            raise ValueError("Недостаточно монет для выполнения операции.")
        self.coins -= amount
