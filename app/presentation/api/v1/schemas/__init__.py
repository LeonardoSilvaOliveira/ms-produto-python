"""
Schemas da API v1 (Request/Response).
"""
from app.presentation.api.v1.schemas.produto_schemas import (
    ProdutoCreateRequest,
    ProdutoUpdateRequest,
    ProdutoResponse,
    ProdutoListResponse,
    MessageResponse,
    ErrorResponse,
)

__all__ = [
    "ProdutoCreateRequest",
    "ProdutoUpdateRequest",
    "ProdutoResponse",
    "ProdutoListResponse",
    "MessageResponse",
    "ErrorResponse",
]