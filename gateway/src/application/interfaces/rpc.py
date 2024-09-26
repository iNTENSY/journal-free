from typing import Protocol, Any

from src.application.interfaces.brokers.rabbitmq.types import RMQExchange


class IRabbitMQRPC(Protocol):
    async def call(self, exchange: RMQExchange, routing_key: str, **parameters) -> Any:
        raise NotImplementedError
