from typing import NewType

import aio_pika.abc

RMQConnection = NewType("RMQConnection", tp=aio_pika.abc.AbstractRobustConnection)
RMQChannel = NewType("RMQChannel", tp=aio_pika.abc.AbstractRobustChannel)
RMQQueue = NewType("RMQQueue", tp=aio_pika.abc.AbstractQueue)
RMQExchange = NewType("RMQExchange", tp=aio_pika.abc.AbstractExchange)

AccountQueue = NewType("AccountQueue", tp=RMQQueue)
