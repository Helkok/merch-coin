from fastapi import APIRouter

from app.api.dependencies import current_user
from app.schemas.schemas import SendCoinRequest
from app.utils.base import BDconnect, TransactionDAO, UserDAO
from app.utils.base import InventoryDAO
from app.utils.constants import MERCH
from app.utils.exceptions import BadRequestError

router = APIRouter()


@router.get("/buy/{item}", summary="Купить предмет за монеты.")
async def buy_item(item: str, session: BDconnect, user: current_user):
    if item not in MERCH:
        raise BadRequestError

    try:
        user.remove_coins(MERCH[item])
    except ValueError:
        raise BadRequestError

    inventory = await InventoryDAO.find_one_or_none_by_filters(session=session, user_id=user.id, item_type=item)

    if inventory:
        inventory.quantity += 1

    else:
        await InventoryDAO.add(session=session, user_id=user.id, item_type=item, quantity=1)

    await session.commit()
    return {"detail": "Успешный ответ."}


@router.post("/sendCoin", summary="Отправить монеты другому пользователю.")
async def send_coin(request: SendCoinRequest, session: BDconnect, user: current_user):
    if request.amount > user.coins:
        raise BadRequestError

    recipient = await UserDAO.find_one_or_none_by_filters(session=session, username=request.toUser)
    if not recipient or recipient.id == user.id:
        raise BadRequestError

    try:
        user.remove_coins(request.amount)
        recipient.add_coins(request.amount)
    except ValueError:
        raise BadRequestError

    await TransactionDAO.add(session=session, sender_id=user.id, receiver_id=recipient.id,
                             amount=request.amount)

    await session.commit()
    return {"detail": "Успешный ответ."}
