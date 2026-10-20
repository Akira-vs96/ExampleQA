from fastapi import APIRouter

from app.api import health, lab7, lab8, lecture7

api_router = APIRouter(prefix="/api")
api_router.include_router(health.router)
api_router.include_router(lecture7.router)
api_router.include_router(lab7.router)
api_router.include_router(lab8.router)
