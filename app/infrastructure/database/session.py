"""
Sessão de banco de dados para injeção de dependência (FastAPI).

Fornece a dependency `get_db` para uso nas routes.
Fica na infraestrutura pois é implementação concreta de como obter sessão.
"""
from typing import Generator

from sqlalchemy.orm import Session

from app.core.database import get_db as core_get_db


# Re-exporta a função get_db do core para manter compatibilidade
# e permitir que a camada de apresentação importe da infraestrutura
get_db = core_get_db


def get_repository_session() -> Generator[Session, None, None]:
    """
    Alias semântico para get_db.

    Uso em factories de repositório:
        def get_produto_repo(db: Session = Depends(get_repository_session)):
            return SQLAlchemyProdutoRepository(db)
    """
    yield from core_get_db()