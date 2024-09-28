class APIException(Exception):
    message: str = "Raised API Exception"

    def __init__(self, message: str = None):
        self.message = message if message else self.message


class TokenExpiredError(APIException):
    message = "Token has expired"


class InvalidTokenPayloadError(APIException):
    message = "Token is not trust"


class InvalidTokenError(APIException):
    message = "Invalid token data"


class ServiceError(APIException):
    message = "Service is unavailable"
