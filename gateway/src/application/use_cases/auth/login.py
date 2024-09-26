from typing import Any

from src.application.dtos.auth.requests import LoginRequest
from src.application.dtos.auth.responses import LoginResponse
from src.application.interfaces.brokers.rabbitmq.types import RMQChannel
from src.application.interfaces.interactor import Interactor
from src.application.interfaces.jwt import IJwtProcessor
from src.infrastructure.brokers.utils.rpc import RabbitMQAsyncRPC


class LoginUseCase(Interactor[LoginRequest, LoginResponse]):
    def __init__(
            self,
            rpc: RabbitMQAsyncRPC,
            channel: RMQChannel,
            jwt_processor: IJwtProcessor
    ) -> None:
        self.__rpc = rpc
        self.__channel = channel
        self.__jwt_processor = jwt_processor

    async def __call__(self, request: LoginRequest) -> LoginResponse:
        account = await self.__get_account(request)
        jwt = self.__jwt_processor.generate_token(account)
        return LoginResponse(access_token=jwt)

    async def __get_account(self, request: LoginRequest) -> dict[str, Any]:
        exchange = await self.__channel.get_exchange("account_exchange")
        account = await self.__rpc.call(
            exchange=exchange,
            routing_key="account",
            method="authorize-client",
            data=vars(request)
        )
        return account
