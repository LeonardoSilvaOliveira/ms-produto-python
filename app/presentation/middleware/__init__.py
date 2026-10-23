"""
Middlewares customizados da aplicação.
"""
from app.presentation.middleware.logging_middleware import LoggingMiddleware

__all__ = ["LoggingMiddleware"]