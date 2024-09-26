from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.infrastructure.di.providers import RabbitMQProvider, SettingsProvider, TimezoneProvider, \
    RMQExchangeProvider, UseCasesProvider, UtilsProvider


def ioc_factory() -> AsyncContainer:
    container = make_async_container(
        SettingsProvider(),
        TimezoneProvider(),
        RabbitMQProvider(),
        RMQExchangeProvider(),
        UseCasesProvider(),
        UtilsProvider()
    )
    return container


def init_di(app: FastAPI) -> None:
    container = ioc_factory()
    setup_dishka(container, app)
