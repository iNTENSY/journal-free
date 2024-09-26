import asyncio
import os

import aio_pika
from dishka import Provider, provide, Scope

from src.application.interfaces.brokers.rabbitmq.types import RMQConnection, RMQChannel, AccountQueue
from src.application.interfaces.jwt import IJwtProcessor
from src.application.interfaces.timezone import IDateTimeProcessor
from src.application.use_cases.auth.login import LoginUseCase
from src.infrastructure.brokers.utils.rpc import RabbitMQAsyncRPC
from src.infrastructure.services.authorization.jwt import JwtProcessor
from src.infrastructure.services.datetimes.timezone import SystemDateTimeProvider, Timezone
from src.infrastructure.settings.jwt import JwtSettings


class SettingsProvider(Provider):
    @provide(scope=Scope.APP, provides=JwtSettings)
    def provide_jwt_settings(self) -> JwtSettings:
        secret_key = "flgnflkgnflkgnfdlkgdklfsnslkfds"
        expires_in = 30 * 60
        algorithm = "HS256"
        return JwtSettings.create(secret=secret_key, expires_in=expires_in, algorithm=algorithm)


class TimezoneProvider(Provider):
    @provide(scope=Scope.APP, provides=IDateTimeProcessor)
    def provide_timezone(self) -> SystemDateTimeProvider:
        return SystemDateTimeProvider(Timezone.MSK)


class RabbitMQProvider(Provider):
    @provide(scope=Scope.APP, provides=RMQConnection)
    async def provide_connection(self) -> aio_pika.abc.AbstractRobustConnection:
        while True:
            try:
                connection = await aio_pika.connect_robust()
                break
            except ConnectionError:
                await asyncio.sleep(5)

        yield connection
        await connection.close()

    @provide(scope=Scope.APP, provides=RMQChannel)
    async def provide_channel(self, connection: RMQConnection) -> aio_pika.abc.AbstractChannel:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            name="account_exchange",
            type=aio_pika.ExchangeType.TOPIC
        )
        account_queue = await channel.declare_queue(name="account-queue")
        await account_queue.bind(exchange, routing_key="account.#")

        log_queue = await channel.declare_queue(name="log-queue")
        await log_queue.bind(exchange, routing_key="#.log")

        yield channel
        await channel.close()

    @provide(scope=Scope.APP, provides=RabbitMQAsyncRPC)
    async def provide_rmq_rpc(self, connection: RMQConnection, channel: RMQChannel):
        rpc = await RabbitMQAsyncRPC().connect(connection, channel)
        return rpc


class RabbitMQRPCProvider(Provider):
    @provide(scope=Scope.APP, provides=RabbitMQAsyncRPC)
    async def provide_rmq_rpc(self, connection: RMQConnection):
        rpc = await RabbitMQAsyncRPC().connect(connection)
        return rpc


class RMQExchangeProvider(Provider):
    @provide(scope=Scope.APP, provides=AccountQueue)
    async def provide_binds_into_account_exchange(self, channel: RMQChannel):
        exchange = await channel.get_exchange("account_exchange")
        account_queue = await channel.get_queue("account-queue")
        log_queue = await channel.get_queue("log-queue")

        await account_queue.bind(exchange, routing_key="#.account.#")
        await log_queue.bind(exchange, routing_key="#.log")


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    login = provide(LoginUseCase)


class UtilsProvider(Provider):
    scope = Scope.APP

    _processor = provide(JwtProcessor, provides=IJwtProcessor)
