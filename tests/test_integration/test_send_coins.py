from async_asgi_testclient import TestClient
import pytest


@pytest.mark.asyncio
async def test_send_money_to_user(client: TestClient, authorization) -> None:
    '''Пользователь отправляет деньги другому пользователю.'''

    response_create_user = await client.post("/api/auth", json={"username": "test", "password": "test"})
    assert response_create_user.status_code == 200

    test_token = response_create_user.json()["token"]
    assert test_token, "Не удалось получить токен для пользователя test."

    sender_info_before = await client.get("/api/info", headers=authorization)
    sender_balance_before = sender_info_before.json()["coins"]

    response_test_user_before = await client.get("/api/info", headers={"Authorization": f"Bearer {test_token}"})
    assert response_test_user_before.status_code == 200
    recipient_balance_before = response_test_user_before.json()["coins"]

    amount_to_send = 1
    response = await client.post("/api/sendCoin", json={"toUser": "test", "amount": amount_to_send},
                                 headers=authorization)

    assert response.status_code == 200
    assert response.json()["detail"] == "Успешный ответ."

    sender_info_after = await client.get("/api/info", headers=authorization)
    sender_balance_after = sender_info_after.json()["coins"]
    assert sender_balance_after == sender_balance_before - amount_to_send

    response_test_user_after = await client.get("/api/info", headers={"Authorization": f"Bearer {test_token}"})
    assert response_test_user_after.status_code == 200
    recipient_balance_after = response_test_user_after.json()["coins"]
    assert recipient_balance_after == recipient_balance_before + amount_to_send


@pytest.mark.asyncio
async def test_send_coin_insufficient_balance(client: TestClient, authorization) -> None:
    '''Проверка ошибки при недостаточном балансе для отправки монет.'''
    response = await client.post("/api/sendCoin", json={"toUser": "test", "amount": 999999}, headers=authorization)
    assert response.status_code == 400
    assert "errors" in response.json()
