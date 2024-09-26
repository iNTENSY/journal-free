import pytest
from httpx import AsyncClient, ASGITransport

from src.presentation.entrypoint import app_factory


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def async_client() -> AsyncClient:
    app = app_factory()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
