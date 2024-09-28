import abc


class BaseHandler(abc.ABC):
    @abc.abstractmethod
    async def handle(self, *args, **kwargs) -> None:
        raise NotImplementedError()
