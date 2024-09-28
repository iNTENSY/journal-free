import abc
import asyncio
import json
import uuid
from typing import Any

import aio_pika.abc

from src.application.interfaces.rpc import IRabbitMQRPC


class RabbitMQAsyncRPC(IRabbitMQRPC):
    connection: aio_pika.abc.AbstractConnection
    channel: aio_pika.abc.AbstractChannel
    callback_queue: aio_pika.abc.AbstractQueue

    def __init__(self):
        self.__futures: dict[str, asyncio.Future] = {}

    async def connect(self, connection: aio_pika.abc.AbstractConnection, channel: aio_pika.abc.AbstractChannel) -> "RabbitMQAsyncRPC":
        self.connection = connection
        self.channel = channel
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        await self.callback_queue.consume(self.__on_response, no_ack=True)
        return self

    async def call(  # noqa
            self,
            exchange: aio_pika.abc.AbstractExchange,
            routing_key: str,
            message_properties: dict[str, Any] = None,
            **parameters
    ) -> Any:
        correlation_id = str(uuid.uuid4())
        future = asyncio.Future()
        self.__futures[correlation_id] = future

        await exchange.publish(
            aio_pika.Message(
                body=json.dumps(parameters).encode(),
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
                **message_properties if message_properties else {}
            ),
            routing_key=routing_key
        )

        return json.loads(await future)

    async def __on_response(self, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        if message.correlation_id is None or message.correlation_id not in self.__futures:
            return

        future = self.__futures.pop(message.correlation_id)
        future.set_result(message.body.decode())
