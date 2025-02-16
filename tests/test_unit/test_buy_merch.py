import pytest

from app.models import User
from app.utils.base import InventoryDAO


@pytest.fixture
def user_with_coins():
    # Возвращаем mock пользователя с 1000 монет
    return User(username="test_user", coins=1000)


def test_buy_item_success(client, user_with_coins, mocker):
    # Мокаем запрос к базе данных для инвентаря
    mocker.patch.object(InventoryDAO, 'find_one_or_none_by_filters', return_value=None)

    item = "t-shirt"  # Покупаем футболку, цена которой 80 монет
    response = client.get(f"/api/buy/{item}", headers={"Authorization": "Bearer test_token"})

    # Проверка корректности выполнения
    assert response.status_code == 200
    assert "Успешный ответ" in response.json().get("detail")


def test_buy_item_insufficient_coins(client, user_with_coins, mocker):
    # Мокаем запрос к базе данных для инвентаря
    mocker.patch.object(InventoryDAO, 'find_one_or_none_by_filters', return_value=None)

    item = "hoody"  # Покупаем худи, цена 300 монет
    user_with_coins.coins = 100  # У пользователя только 100 монет

    response = client.get(f"/api/buy/{item}", headers={"Authorization": "Bearer test_token"})

    assert response.status_code == 400
