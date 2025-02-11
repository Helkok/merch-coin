from typing import List

from pydantic import BaseModel, Field


class InventoryItem(BaseModel):
    type: str = Field(..., description="Тип предмета.")
    quantity: int = Field(..., description="Количество предметов.")


class CoinTransactionReceived(BaseModel):
    fromUser: str = Field(..., description="Имя пользователя, который отправил монеты.")
    amount: int = Field(..., description="Количество полученных монет.")


class CoinTransactionSent(BaseModel):
    toUser: str = Field(..., description="Имя пользователя, которому отправлены монеты.")
    amount: int = Field(..., description="Количество отправленных монет.")


class CoinHistory(BaseModel):
    received: List[CoinTransactionReceived] = Field(..., description="История полученных монет.")
    sent: List[CoinTransactionSent] = Field(..., description="История отправленных монет.")


class InfoResponse(BaseModel):
    coins: int = Field(..., description="Количество доступных монет.")
    inventory: List[InventoryItem] = Field(..., description="Список предметов в инвентаре.")
    coinHistory: CoinHistory


class SendCoinRequest(BaseModel):
    toUser: str = Field(..., description="Имя пользователя, которому нужно отправить монеты.")
    amount: int = Field(..., description="Количество монет, которые необходимо отправить.")


class AuthRequest(BaseModel):
    username: str = Field(..., description="Имя пользователя для аутентификации.")
    password: str = Field(..., description="Пароль для аутентификации.")


class AuthResponse(BaseModel):
    token: str = Field(..., description="JWT-токен для доступа к защищенным ресурсам.")


class ErrorResponse(BaseModel):
    errors: str = Field(..., description="Сообщение об ошибке, описывающее проблему.")
