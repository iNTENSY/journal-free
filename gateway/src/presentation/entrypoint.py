import uvicorn
from fastapi import FastAPI

from src.infrastructure.di.container import init_di
from src.presentation.exc_hanlers import init_exc_handlers
from src.presentation.v1.router import v1_router


def init_routers(app: FastAPI) -> None:
    routers = (v1_router,)

    for router in routers:
        app.include_router(router)


def app_factory() -> FastAPI:
    app = FastAPI()
    init_di(app)
    init_routers(app)
    init_exc_handlers(app)
    return app


if __name__ == '__main__':
    uvicorn.run("src.presentation.entrypoint:app_factory", factory=True)
