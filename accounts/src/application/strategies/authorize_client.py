import json
import sys
from typing import Any

import aio_pika
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.handlers import IAuthorizeClientHandler
from src.application.strategies.core import BaseHandler


class AuthorizeClientHandler(BaseHandler, IAuthorizeClientHandler):
    def __init__(self, connection: AsyncSession):
        self.__connection = connection

    async def handle(self, *args, **kwargs) -> None:
        message: aio_pika.abc.AbstractIncomingMessage = kwargs.get("message")
        decoded_data: dict[str, Any] = kwargs.get("decoded_message")
        channel: aio_pika.abc.AbstractChannel = kwargs.get("channel")
        sys.stdout.write(f"Got method `authorize-client`: {decoded_data}")

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps({"username": "username", "email": "email@example.ru"}).encode(),
                correlation_id=message.correlation_id,
                expiration=10
            ),
            routing_key=message.reply_to
        )
