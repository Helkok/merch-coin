import time

import pytest

from app.core.security import create_access_token, hash_password, verify_access_token, verify_password
from app.models.user import User


def test_hash_password():
    '''Тест хеширования пароля.'''
    user = User(username="test_user", password_hash="test_password")
    user.password = hash_password(user.password_hash)
    assert user.password != "test_password"


def test_verify_password():
    '''Тест проверки пароля.'''
    user = User(username="test_user", password_hash="test_password")
    user.password_hash = hash_password(user.password_hash)
    assert verify_password("test_password", user.password_hash) == True
    assert verify_password("wrong_password", user.password_hash) == False


def test_create_access_token():
    '''Тест создания токена.'''
    user = User(username="test_user", password_hash="test_password")
    token = create_access_token({"sub": user.username})
    assert token is not None
    assert token != "test_token"


def test_verify_access_token():
    user = User(username="test_user", password_hash="test_password")
    token = create_access_token({"sub": user.username})

    # Проверка валидного токена
    decoded_token = verify_access_token(token)
    assert decoded_token is not None
    assert decoded_token["sub"] == user.username
    assert "exp" in decoded_token  # Проверка, что ключ "exp" существует в декодированном токене

    decoded_token = verify_access_token("wrong_token")
    assert decoded_token is None


def test_hash_empty_password():
    '''Тест пустого пароля.'''
    user = User(username="test_user", password_hash="")
    user.password = hash_password(user.password_hash)
    assert user.password != ""


def test_verify_empty_token():
    '''Тест пустого токена.'''
    decoded_token = verify_access_token("")
    assert decoded_token is None


def test_create_access_token_unique():
    '''Тест уникальности токенов.'''
    user = User(username="test_user", password_hash="test_password")
    token1 = create_access_token({"sub": user.username})
    time.sleep(1)  # Ждем 1 секунду, чтобы время создания токенов было разным
    token2 = create_access_token({"sub": user.username})
    assert token1 != token2  # Токены должны быть разными


def test_hash_same_password_twice():
    '''Тест хеширования одного и того же пароля дважды.'''
    password = "test_password"
    hashed_password1 = hash_password(password)
    hashed_password2 = hash_password(password)
    assert hashed_password1 != hashed_password2


def test_method_add_coins():
    '''Тест метода add_coins класса User.'''
    user = User(username="test_user", password_hash="test_password")
    user.coins = 0
    user.add_coins(100)
    assert user.coins == 100
    user.add_coins(50)
    assert user.coins == 150
    with pytest.raises(ValueError, match="Количество монет должно быть больше 0."):
        user.add_coins(-100)  # Пытаемся добавить отрицательное количество монет
    assert user.coins == 150


def test_method_remove_coins():
    '''Тест метода remove_coins класса User.'''
    user = User(username="test_user", password_hash="test_password")
    user.coins = 100
    user.remove_coins(50)  # Удаляем 50 монет
    assert user.coins == 50
    with pytest.raises(ValueError, match="Недостаточно монет для выполнения операции."):
        user.remove_coins(100)  # Пытаемся удалить 100 монет, хотя у пользователя их всего 50
    assert user.coins == 50
    with pytest.raises(ValueError, match="Количество монет должно быть больше 0."):
        user.remove_coins(-100)  # Пытаемся удалить отрицательное количество монет
    assert user.coins == 50
