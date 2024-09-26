import datetime as dt
from typing import Any

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError

from src.application.interfaces.jwt import IJwtProcessor
from src.application.interfaces.timezone import IDateTimeProcessor
from src.infrastructure.services.exceptions.custom_exceptions import InvalidTokenPayloadError, TokenExpiredError, \
    InvalidTokenError
from src.infrastructure.settings.jwt import JwtSettings


class JwtProcessor(IJwtProcessor):
    def __init__(
            self,
            settings: JwtSettings,
            dt_processor: IDateTimeProcessor
    ) -> None:
        self.__settings = settings
        self.__dt = dt_processor
        self.__current_datetime = self.__dt.get_current_time()

    def generate_token(self, credentials: dict[str, Any]) -> str:
        issued_at = self.__current_datetime
        expiration_time = issued_at + dt.timedelta(seconds=self.__settings.expires_in)

        payload = {
            "iat": issued_at,
            "exp": expiration_time
        }
        payload.update(credentials)

        encoded_jwt = jwt.encode(payload, key=self.__settings.secret, algorithm=self.__settings.algorithm)
        return encoded_jwt

    def parse(self, token: str,) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, key=self.__settings.secret, algorithms=self.__settings.algorithm)
            return payload
        except ExpiredSignatureError:
            raise TokenExpiredError
        except JWTClaimsError:
            raise InvalidTokenPayloadError
        except JWTError:
            raise InvalidTokenError

    def refresh_token(self, token: str) -> str:
        payload = self.parse(token)
        return self.generate_token(*payload)
