import asyncio
from typing import AsyncGenerator, Generator

from async_asgi_testclient import TestClient
import pytest
import pytest_asyncio

from app.main import app


@pytest.fixture(autouse=True, scope="session")
def run_migration():
    import os
    os.system("alembic upgrade head")
    yield
    os.system("alembic downgrade base")


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[TestClient, None]:
    host, port = "127.0.0.1", 8000
    scope = {"client": (host, port)}

    async with TestClient(app, scope=scope) as client:
        yield client


@pytest_asyncio.fixture
async def authorization(client: TestClient) -> dict[str, str]:
    response = await client.post("/api/auth", json={"username": "register2", "password": "register"})
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}
