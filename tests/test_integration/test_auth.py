from async_asgi_testclient import TestClient
import pytest


@pytest.mark.asyncio
async def test_register(client: TestClient) -> None:
    '''Пользователь уже зарегистрирован'''
    response = await client.post("/api/auth", json={"username": "register", "password": "register"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_auth_invalid_credentials(client: TestClient, authorization) -> None:
    '''Неверный токен.'''
    response = await client.post("/api/auth", json={"username": "register", "password": "wrong_password"},
                                 headers=authorization)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_access(client: TestClient) -> None:
    '''Проверка доступа без авторизации.'''
    response = await client.get("/api/info")
    assert response.status_code == 401
    assert "errors" in response.json()
