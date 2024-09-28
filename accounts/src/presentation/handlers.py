import json
from typing import Generic, TypeVar, Type

import aio_pika

from src.application.interfaces.types import RMQChannel
from src.application.strategies.core import BaseHandler


class AccountQueueActionHandler:
    def __init__(
            self,
            channel: RMQChannel,
            queue: aio_pika.abc.AbstractQueue,
            actions: dict[str, BaseHandler]
    ) -> None:
        self.__actions = actions
        self.channel = channel
        self.queue = queue

    async def start(self):
        await self.queue.consume(self.handle)

    async def handle(self, message: aio_pika.abc.AbstractIncomingMessage):
        decoded_message = json.loads(message.body.decode())
        correlation_id = message.correlation_id
        method = decoded_message["method"]

        action = self.__actions.get(method, None)
        if not action:
            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=f"Invalid method ({method})".encode(),
                    correlation_id=correlation_id
                ),
                routing_key=message.reply_to
            )
            return
        await action.handle(
            message=message,
            decoded_message=decoded_message,
            channel=self.channel,
        )
