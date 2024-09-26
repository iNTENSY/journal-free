from typing import Protocol, Any


class IJwtProcessor(Protocol):
    def generate_token(self, credentials: dict[str, Any]) -> str:
        raise NotImplementedError

    def parse(self, token: str) -> dict[str, Any]:
        raise NotImplementedError

    def refresh_token(self, token: str) -> str:
        raise NotImplementedError
