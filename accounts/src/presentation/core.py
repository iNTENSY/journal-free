import asyncio
import sys


class Application:
    def __init__(self):
        self.__broker = None
        self.__ioc = None

    @property
    def broker(self):
        return self.__broker

    @broker.setter
    def broker(self, _broker):
        self.__broker = _broker

    @property
    def container(self):
        return self.__ioc

    @container.setter
    def container(self, _container):
        self.__ioc = _container

    async def run(self):
        sys.stdout.write("[Account service] Trying to start all consumers...\n")
        for handler in self.__broker.queues:
            await handler.start()
        sys.stdout.write("[Account service] Service is ready to consume...\n")
        await asyncio.Event().wait()
