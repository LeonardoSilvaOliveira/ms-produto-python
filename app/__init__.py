"""
MS Produtos - Microsserviço de gerenciamento de produtos.

Arquitetura Limpa (Clean Architecture) com FastAPI.
"""
from app.main import app, create_app

__version__ = "1.0.0"

__all__ = ["app", "create_app"]