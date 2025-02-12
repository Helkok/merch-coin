from fastapi import APIRouter

from app.schemas.schemas import *
from app.utils.base import BDconnect, UserDAO
from app.utils.exceptions import UnauthorizedError
from app.utils.utils import create_access_token, verify_password

router = APIRouter()


@router.post("/auth",
             summary="Аутентификация и получение JWT-токена.",
             response_model=AuthResponse)
async def auth(request: AuthRequest, db: BDconnect):
    user = await UserDAO.find_one_or_none_by_filters(session=db, username=request.username)
    if not user:
        await UserDAO.add_user(session=db, values=request)
        access_token = create_access_token({"sub": str(user.username)})
        return {"token": access_token}
    if not verify_password(request.password, user.password_hash):
        raise UnauthorizedError
    access_token = create_access_token({"sub": str(user.username)})
    return {"token": access_token}
