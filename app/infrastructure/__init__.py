"""
Camada de Infraestrutura - Implementações concretas.

Contém:
- Models SQLAlchemy (models/)
- Repositories implementations (repositories/)
- Database session management (database/)
"""
from app.infrastructure.models import ProdutoModel
from app.infrastructure.repositories import SQLAlchemyProdutoRepository
from app.infrastructure.database import get_db, get_repository_session

__all__ = [
    "ProdutoModel",
    "SQLAlchemyProdutoRepository",
    "get_db",
    "get_repository_session",
]