from fastapi import APIRouter
from app.api.v1.endpoints import analyze, compare   # 👈 ADD compare

api_router = APIRouter()

# Register analyze router
api_router.include_router(analyze.router, prefix='/analyze', tags=['analyze'])

# 👇 ADD THIS BLOCK
api_router.include_router(compare.router, prefix='/compare', tags=['compare'])