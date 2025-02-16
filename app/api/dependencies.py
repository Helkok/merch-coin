from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import verify_access_token
from app.models import User
from app.utils.base import BDconnect, UserDAO
from app.utils.exceptions import UnauthorizedError

token_bearer = HTTPBearer(auto_error=False)


# Функция для извлечения токена из заголовков
async def get_access_token(credentials: HTTPAuthorizationCredentials = Depends(token_bearer)):
    if credentials is None or not credentials.credentials:
        raise UnauthorizedError
    return credentials.credentials


# Проверка и верификация токена
def verify_token_expiration(token: str):
    try:
        payload = verify_access_token(token)
    except Exception:
        raise UnauthorizedError
    if payload is None:
        raise UnauthorizedError

    # Проверяем срок действия токена
    expire: str = payload.get("exp")
    if not expire:
        raise UnauthorizedError

    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if expire_time < datetime.now(timezone.utc):
        raise UnauthorizedError

    return payload


async def get_current_user(session: BDconnect, token: str = Depends(get_access_token)):
    'Получение текущего пользователя'
    payload = verify_token_expiration(token)  # Проверка токена и его срока действия

    username: str = payload.get("sub")
    if not username:
        raise UnauthorizedError

    user = await UserDAO.find_one_or_none_by_filters(session, username=username)
    if not user:
        raise UnauthorizedError

    return user


current_user = Annotated[User, Depends(get_current_user)]
