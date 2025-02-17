from async_asgi_testclient import TestClient
import pytest


@pytest.mark.asyncio
async def test_info_user(client: TestClient, authorization) -> None:
    '''Пользователь просматривает свою информацию.'''
    response = await client.get("/api/info", headers=authorization)
    assert response.status_code == 200
    assert "coins" in response.json()
    assert "inventory" in response.json()
    assert "coinHistory" in response.json()
