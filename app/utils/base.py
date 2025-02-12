from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.models import *
from app.schemas.schemas import AuthRequest
from app.utils.utils import hash_password

BDconnect = Annotated[AsyncSession, Depends(get_session)]


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none_by_filters(cls, session: AsyncSession, **filters):
        '''Функция для поиска одного объекта по фильтрам'''
        result = await session.execute(select(cls.model).filter_by(**filters))
        return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, session: AsyncSession):
        '''Функция для поиска всех объектов'''
        result = await session.execute(select(cls.model))
        return result.scalars().all()

    @classmethod
    async def find_all_by_filters(cls, session: AsyncSession, **filters):
        '''Функция для поиска всех объектов по фильтрам'''
        result = await session.execute(select(cls.model).filter_by(**filters))
        return result.scalars().all()


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def add_user(cls, session: AsyncSession, values: AuthRequest):
        '''Функция для добавления пользователя в базу данных'''
        hashed_password = hash_password(values.password)
        new_user = cls.model(username=values.username, password_hash=hashed_password)
        session.add(new_user)
        await session.commit()
        return new_user


class InventoryDAO(BaseDAO):
    model = Inventory


class TransactionDAO(BaseDAO):
    model = Transaction
