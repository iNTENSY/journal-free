from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseSettings:
    db_url: str

    @staticmethod
    def create(url) -> "DatabaseSettings":
        return DatabaseSettings(url)
