from app.schemas.schemas import AuthResponse, ErrorResponse

RESPONSES = {
    200: {
        "description": "Успешный ответ.",
        "model": AuthResponse,
    },
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
    },
}
