"""
API v1 - Rotas e Schemas.
"""
from app.presentation.api.v1.routes import produtos_router
from app.presentation.api.v1.schemas import (
    ProdutoCreateRequest,
    ProdutoUpdateRequest,
    ProdutoResponse,
    ProdutoListResponse,
    MessageResponse,
    ErrorResponse,
)

__all__ = [
    "produtos_router",
    "ProdutoCreateRequest",
    "ProdutoUpdateRequest",
    "ProdutoResponse",
    "ProdutoListResponse",
    "MessageResponse",
    "ErrorResponse",
]