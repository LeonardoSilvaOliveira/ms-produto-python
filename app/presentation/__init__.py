"""
Camada de Apresentação - API HTTP.

Contém:
- API routes e schemas (api/)
- Dependencies/Injeção de dependência (api/deps.py)
- Middlewares customizados (middleware/)
"""
from app.presentation.api import produtos_router
from app.presentation.api.deps import get_produto_service, get_produto_repository
from app.presentation.middleware import LoggingMiddleware

__all__ = [
    "produtos_router",
    "get_produto_service",
    "get_produto_repository",
    "LoggingMiddleware",
]