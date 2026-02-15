"""
API Routes for CloudSpend AI
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy"}
