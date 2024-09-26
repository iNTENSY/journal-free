from fastapi import APIRouter

from src.presentation.v1.auth import router as auth_router


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(auth_router)
