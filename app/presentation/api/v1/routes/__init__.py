"""
Routes da API v1.
"""
from app.presentation.api.v1.routes.produtos import router as produtos_router

__all__ = ["produtos_router"]