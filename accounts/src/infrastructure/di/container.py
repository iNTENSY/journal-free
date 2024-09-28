from dishka import AsyncContainer, make_async_container

from src.infrastructure.di.providers import RepositoriesProvider, SQLAlchemyProvider, ActionHandlersProvider, \
    RabbitMQProvider, MethodsHandlerProvider


def ioc_factory() -> AsyncContainer:
    return make_async_container(
        SQLAlchemyProvider(),
        RepositoriesProvider(),
        RabbitMQProvider(),
        MethodsHandlerProvider(),
        ActionHandlersProvider()
    )
