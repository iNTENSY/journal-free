from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.responses import Response

from src.application.dtos.auth.requests import LoginRequest
from src.application.dtos.auth.responses import LoginResponse
from src.application.use_cases.auth.login import LoginUseCase

router = APIRouter(prefix="/auth", route_class=DishkaRoute)


@router.post(
    path="/login",
    response_model=LoginResponse
)
async def authorize_route(
        request: LoginRequest,
        response: Response,
        interactor: FromDishka[LoginUseCase],
) -> LoginResponse:
    auth_response = await interactor(request)
    response.set_cookie(key="access_token", value=f"Bearer {auth_response.access_token}", httponly=True)
    return auth_response
