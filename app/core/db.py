from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, future=True, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, )
DATABASE_URL = settings.DATABASE_URL


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    pass


async def get_session():
    """Получение сессии для работы с БД."""
    async with async_session_maker() as session:
        yield session
