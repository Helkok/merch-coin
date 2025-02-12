from fastapi import HTTPException, status

from app.schemas.schemas import AuthResponse, ErrorResponse

RESPONSES = {
    200: {
        "description": "Успешная аутентификация.",
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


class BadRequestError(HTTPException):
    '''Класс ошибки 400 для неверного запроса.'''
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный запрос."


class UnauthorizedError(HTTPException):
    '''Класс ошибки 401 для неавторизованного пользователя.'''
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неавторизован."


class InternalServerError(HTTPException):
    '''Класс ошибки 500 для внутренней ошибки сервера.'''
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Внутренняя ошибка сервера."
