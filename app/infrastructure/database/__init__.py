"""
Configuração de banco de dados da infraestrutura.
"""
from app.infrastructure.database.session import get_db, get_repository_session

__all__ = ["get_db", "get_repository_session"]