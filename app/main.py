"""
Entry point da aplicação - MS Produtos.

Configura FastAPI, middlewares, routers e ciclo de vida.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import create_tables
from app.presentation.api import produtos_router
from app.presentation.middleware import LoggingMiddleware

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia ciclo de vida da aplicação.

    Startup: Cria tabelas (desenvolvimento) ou roda migrações (produção)
    Shutdown: Cleanup se necessário
    """
    # Startup
    if settings.ENVIRONMENT == "development":
        # Em desenvolvimento, cria tabelas automaticamente
        # Em produção, usar: alembic upgrade head
        create_tables()

    yield

    # Shutdown
    # Adicionar cleanup se necessário (fechar conexões, etc.)


def create_app() -> FastAPI:
    """
    Factory para criar instância da aplicação FastAPI.

    Permite criar múltiplas instâncias para testes.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Microsserviço de Produtos - Clean Architecture",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Middleware de logging
    app.add_middleware(LoggingMiddleware)

    # Health check
    @app.get("/", tags=["Health"])
    async def health_check():
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        }

    @app.get("/health", tags=["Health"])
    async def health():
        """Health check simples para load balancers."""
        return {"status": "ok"}

    # Incluir routers da API v1
    app.include_router(
        produtos_router,
        prefix=settings.API_PREFIX,
    )

    return app


# Instância global da aplicação
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )