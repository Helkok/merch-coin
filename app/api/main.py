from fastapi import APIRouter

from app.api.routers.auth import router as auth_router
from app.api.routers.transactions import router as transaction_router
from app.api.routers.user_info import router as user_router
from app.utils.constants import RESPONSES

api_router = APIRouter()

api_router.include_router(auth_router, tags=["auth"], responses=RESPONSES)
api_router.include_router(transaction_router, tags=["transactions"], responses=RESPONSES)
api_router.include_router(user_router, tags=["users"], responses=RESPONSES)
