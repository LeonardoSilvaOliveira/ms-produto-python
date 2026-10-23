"""
Middleware de logging para requisições HTTP.

Registra informações de cada request/response para observabilidade.
"""
import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.config import get_settings

settings = get_settings()


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para logging de requisições.

    Adiciona:
    - Request ID único para rastreamento
    - Tempo de processamento
    - Log de entrada e saída
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Gerar request ID único
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id

        # Log de entrada
        start_time = time.perf_counter()

        # Em produção, usar structlog ou logger configurado
        if settings.DEBUG:
            print(
                f"[{request_id}] -> {request.method} {request.url.path} "
                f"from {request.client.host if request.client else 'unknown'}"
            )

        try:
            response = await call_next(request)
        except Exception as e:
            # Log de erro
            process_time = time.perf_counter() - start_time
            if settings.DEBUG:
                print(
                    f"[{request_id}] <- {request.method} {request.url.path} "
                    f"ERROR ({process_time:.3f}s): {type(e).__name__}: {e}"
                )
            raise

        # Log de saída
        process_time = time.perf_counter() - start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.3f}"

        if settings.DEBUG:
            print(
                f"[{request_id}] <- {request.method} {request.url.path} "
                f"{response.status_code} ({process_time:.3f}s)"
            )

        return response