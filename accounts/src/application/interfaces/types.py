from typing import NewType

import aio_pika.abc

RMQConnection = NewType("RMQConnection", tp=aio_pika.abc.AbstractConnection)
RMQChannel = NewType("RMQChannel", tp=aio_pika.abc.AbstractChannel)
