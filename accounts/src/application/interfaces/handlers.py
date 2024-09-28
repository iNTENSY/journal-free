from typing import Protocol, Any


class IAuthorizeClientHandler(Protocol):
    async def handle(self, *args, **kwargs) -> Any:
        raise NotImplementedError
