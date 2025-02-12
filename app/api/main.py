from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.utils.constants import RESPONSES

api_router = APIRouter()

api_router.include_router(auth_router, tags=["auth"], responses=RESPONSES)
