from httpx import ASGITransport, AsyncClient
import pytest
import pytest_asyncio

from app.core.db import async_session_maker, get_session
from app.main import app
from app.utils.base import InventoryDAO, UserDAO


@pytest_asyncio.fixture
async def session():
    async for item in get_session():
        yield item


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client


async def auth_token(async_client, username):
    user_data = {
        "username": username,
        "password": "test_password"
    }
    response = await async_client.post("/api/auth", json=user_data)
    assert response.status_code == 200
    return response.json().get("token")


@pytest.mark.asyncio
async def test_buy_item_success(async_client):
    '''Тест на успешную покупку предмета.'''
    token = await auth_token(async_client, "test_buy_item_success")
    async with async_session_maker() as session:
        user = await UserDAO.find_one_or_none_by_filters(session=session, username="test_buy_item_success")
        user.coins = 1000
        user_inventory = await InventoryDAO.find_one_or_none_by_filters(session=session, user_id=user.id,
                                                                        item_type="t-shirt")
        if user_inventory:
            await session.delete(user_inventory)
        await session.commit()

    item = "t-shirt"
    response = await async_client.get(f"/api/buy/{item}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

    async with async_session_maker() as session:
        user2 = await UserDAO.find_one_or_none_by_filters(session=session, username="test_buy_item_success")
        user_inventory = await InventoryDAO.find_one_or_none_by_filters(session=session, user_id=user.id,
                                                                        item_type="t-shirt")
        assert user_inventory.quantity == 1
        assert user2.coins == 920
