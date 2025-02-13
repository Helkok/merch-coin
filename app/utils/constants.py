from app.schemas.schemas import ErrorResponse

RESPONSES = {
    400: {
        "description": "Неверный запрос.",
        "model": ErrorResponse,
    },
    401: {
        "description": "Неавторизован.",
        "model": ErrorResponse,
    },
    500: {
        "description": "Внутренняя ошибка сервера.",
        "model": ErrorResponse,
    }
}

MERCH = {
    "t-shirt": 80,
    "cup": 20,
    "book": 50,
    "pen": 10,
    "powerbank": 200,
    "hoody": 300,
    "umbrella": 200,
    "socks": 10,
    "wallet": 50,
    "pink-hoody": 500
}
