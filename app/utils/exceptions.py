from fastapi import HTTPException, status

from app.schemas.schemas import ErrorResponse


class CustomHTTPException(HTTPException):
    """Базовый класс для всех кастомных исключений."""
    status_code: int
    detail: ErrorResponse

    def __init__(self, detail: ErrorResponse = None):
        if detail is None:
            detail = ErrorResponse(errors=self.detail)
        super().__init__(status_code=self.status_code, detail=detail)


class BadRequestError(CustomHTTPException):
    '''Класс ошибки 400 для неверного запроса.'''
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный запрос."


class UnauthorizedError(CustomHTTPException):
    '''Класс ошибки 401 для неавторизованного пользователя.'''
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Необходима авторизация."


class InternalServerError(CustomHTTPException):
    '''Класс ошибки 500 для внутренней ошибки сервера.'''
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Внутренняя ошибка сервера."
