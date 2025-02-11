from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, future=True, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, )
DATABASE_URL = settings.DATABASE_URL


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    pass


async def get_session():
    '''Функция для получения сессии базы данных. Вызывается в зависимостях FastAPI'''
    async with async_session_maker() as session:
        yield session

