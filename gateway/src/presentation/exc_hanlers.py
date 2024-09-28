from dataclasses import dataclass
from typing import Annotated

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from src.infrastructure.services.exceptions.custom_exceptions import TokenExpiredError, APIException, ServiceError


@dataclass
class ExceptionHandler:
    status_code: int
    custom_content: str | None = None

    async def __call__(self, request: Request, exc: Exception) -> Response:
        response = {"detail": exc.message} if not self.custom_content else self.custom_content
        return JSONResponse(content=response, status_code=self.status_code)


def init_exc_handlers(app: FastAPI):
    exceptions = (
        (TokenExpiredError, ExceptionHandler(status_code=status.HTTP_403_FORBIDDEN)),
        (ServiceError, ExceptionHandler(status_code=status.HTTP_400_BAD_REQUEST))
    )

    for exception, handler in exceptions:
        app.add_exception_handler(exception, handler)
