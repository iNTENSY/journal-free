import asyncio

from src.infrastructure.services.exceptions.custom_exceptions import ServiceError


def wait_for(timeout: int = None):
    def outer(func):
        async def inner(*args, **kwargs):
            task = asyncio.create_task(func(*args, **kwargs))

            try:
                result = await asyncio.wait_for(task, timeout=timeout)
            except asyncio.TimeoutError:
                raise ServiceError

            return result
        return inner
    return outer
