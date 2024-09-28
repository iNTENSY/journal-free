import sys
from os.path import dirname

import asyncio

from dotenv import load_dotenv

sys.path.insert(0, dirname(dirname(dirname(__file__))))

from src.infrastructure.broker.rabbit.core import init_rabbitmq
from src.infrastructure.di.container import ioc_factory
from src.presentation.core import Application

load_dotenv(".env")


async def main():
    app = Application()
    app.container = ioc_factory()
    await init_rabbitmq(app)
    await app.run()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
