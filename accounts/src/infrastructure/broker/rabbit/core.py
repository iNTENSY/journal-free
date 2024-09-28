from src.application.interfaces.types import RMQConnection, RMQChannel
from src.presentation.core import Application
from src.presentation.handlers import AccountQueueActionHandler


class RabbitMQBroker:
    def __init__(self, connection: RMQConnection, channel: RMQChannel):
        self.connection = connection
        self.channel = channel
        self.__queues: list[AccountQueueActionHandler] = []

    def add_queue_handlers(self, handler: AccountQueueActionHandler):
        self.__queues.append(handler)

    @property
    def queues(self):
        return self.__queues


async def init_rabbitmq(app: Application):
    async with app.container() as container:
        connection = await container.get(RMQConnection)
        channel = await container.get(RMQChannel)
        account_action_handler = await container.get(AccountQueueActionHandler)
    broker = RabbitMQBroker(connection, channel)
    broker.add_queue_handlers(account_action_handler)
    app.broker = broker
