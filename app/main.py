from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi

from app.api.main import api_router


def create_app() -> FastAPI:
    """Создание FastAPI-приложения с кастомной конфигурацией."""
    app = FastAPI(title="API Avito shop", version="1.0.0")

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid request data", "errors": exc.errors()},
        )

    def custom_openapi():
        """Генерация OpenAPI-схемы без 422 ошибок."""
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="API Avito shop",
            version="1.0.0",
            routes=app.routes,
        )
        # Удаляем 422 ошибки из документации
        for path in openapi_schema["paths"]:
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["responses"].pop("422", None)

        app.openapi_schema = openapi_schema
        return openapi_schema

    app.openapi = custom_openapi

    app.include_router(api_router, prefix="/api")

    return app


app = create_app()
