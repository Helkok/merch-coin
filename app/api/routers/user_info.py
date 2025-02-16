from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.dependencies import current_user
from app.models import Transaction, User
from app.schemas.schemas import CoinTransactionReceived, CoinTransactionSent, InfoResponse, InventoryItem
from app.utils.base import BDconnect

router = APIRouter()


@router.get("/info", summary="Получить информацию о монетах, инвентаре и истории транзакций.",
            response_model=InfoResponse)
async def info(session: BDconnect, user_cur: current_user):
    stmt = select(User).options(
        selectinload(User.inventory),
        selectinload(User.transactions_sent).selectinload(Transaction.receiver),
        selectinload(User.transactions_received).selectinload(Transaction.sender)
    ).filter(User.id == user_cur.id)

    result = await session.execute(stmt)

    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    validated_inventory = [
        InventoryItem(type=item.item_type, quantity=item.quantity) for item in user.inventory
    ]

    validated_sent_transactions = [
        CoinTransactionSent(toUser=transaction.receiver.username, amount=transaction.amount)
        for transaction in user.transactions_sent
    ]

    validated_received_transactions = [
        CoinTransactionReceived(fromUser=transaction.sender.username, amount=transaction.amount)
        for transaction in user.transactions_received
    ]

    return InfoResponse(
        coins=user.coins,
        inventory=validated_inventory,
        coinHistory={
            "received": validated_received_transactions,
            "sent": validated_sent_transactions
        }
    )
