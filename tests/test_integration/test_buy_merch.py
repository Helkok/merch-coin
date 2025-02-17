from async_asgi_testclient import TestClient
import pytest


@pytest.mark.asyncio
async def test_buy_merch(client: TestClient, authorization) -> None:
    '''Пользователь покупает предмет.'''
    response = await client.get("/api/buy/cup", headers=authorization)
    assert response.status_code == 200
    assert response.json()["detail"] == "Успешный ответ."
