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

    # Добавление каскадного удаления для транзакций и инвентаря
    transactions_sent: Mapped[List["Transaction"]] = relationship("Transaction", foreign_keys="Transaction.sender_id",
                                                                  back_populates="sender", cascade="all, delete-orphan")
    transactions_received: Mapped[List["Transaction"]] = relationship("Transaction",
                                                                      foreign_keys="Transaction.receiver_id",
                                                                      back_populates="receiver",
                                                                      cascade="all, delete-orphan")
    inventory: Mapped[List["Inventory"]] = relationship("Inventory", back_populates="user",
                                                        cascade="all, delete-orphan")

    def add_coins(self, amount: int):
        """Добавляет монеты к балансу пользователя."""
        self.validate_amount(amount)
        new_balance = self.coins + amount
        # Можно добавить проверку на переполнение
        if new_balance < 0:
            raise ValueError("Недостаточно монет для выполнения операции.")
        self.coins = new_balance

    def remove_coins(self, amount: int):
        """Удаляет монеты из баланса пользователя"""
        self.validate_amount(amount)
        if self.coins - amount < 0:
            raise ValueError("Недостаточно монет для выполнения операции.")
        self.coins -= amount

    def validate_amount(self, amount: int):
        """Проверяет, что количество монет больше 0"""
        if amount <= 0:
            raise ValueError("Количество монет должно быть больше 0.")

    def get_balance(self) -> int:
        """Возвращает текущий баланс пользователя."""
        return self.coins
