import asyncio
import os

import aio_pika
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession, create_async_engine

from src.application.interfaces.handlers import IAuthorizeClientHandler
from src.application.interfaces.types import RMQConnection, RMQChannel
from src.application.strategies.authorize_client import AuthorizeClientHandler
from src.domain.accounts.repository import IAccountRepository
from src.infrastructure.persistence.repositories.account import AccountRepositoryImp
from src.infrastructure.settings.database import DatabaseSettings
from src.presentation.handlers import AccountQueueActionHandler


class SQLAlchemyProvider(Provider):
    @provide(scope=Scope.APP, provides=DatabaseSettings)
    def provide_settings(self) -> DatabaseSettings:
        url = "postgresql+asyncpg://postgres:postgres@accounts_db:5432/journal-account-microservice-database"
        return DatabaseSettings.create(url)

    @provide(scope=Scope.APP, provides=AsyncEngine)
    def provide_engine(self, settings: DatabaseSettings) -> AsyncEngine:
        return create_async_engine(settings.db_url)

    @provide(scope=Scope.APP, provides=async_sessionmaker[AsyncSession])
    def provide_session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncSession:
        async with session_maker() as session:
            yield session


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    account_repo = provide(source=AccountRepositoryImp, provides=IAccountRepository)


class RabbitMQProvider(Provider):
    @provide(scope=Scope.APP, provides=RMQConnection)
    async def provide_rmq_connection(self) -> RMQConnection:
        url = f"amqp://guest:guest@rabbitmq:5672/"
        while True:
            try:
                connection = await aio_pika.connect_robust(url=url)
                break
            except ConnectionError:
                await asyncio.sleep(5)

        yield connection
        await connection.close()

    @provide(scope=Scope.APP, provides=RMQChannel)
    async def provide_channel(self, connection: RMQConnection) -> RMQChannel:
        channel = await connection.channel()
        await channel.declare_queue("account-queue")
        async with channel:
            yield channel


class MethodsHandlerProvider(Provider):
    scope = Scope.REQUEST
    authorize_client = provide(AuthorizeClientHandler, provides=IAuthorizeClientHandler)


class ActionHandlersProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=AccountQueueActionHandler)
    async def provide_handler(
            self,
            channel: RMQChannel,
            authorize_handler: IAuthorizeClientHandler
    ) -> AccountQueueActionHandler:
        queue = await channel.get_queue("account-queue")

        actions = {
            "authorize-client": authorize_handler
        }
        return AccountQueueActionHandler(channel, queue, actions)
