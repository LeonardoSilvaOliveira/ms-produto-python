"""
Dependencies (Injeção de Dependência) para FastAPI.

Centraliza a criação e fornecimento de dependências para as routes.
Segue o princípio de Inversão de Controle (IoC).
"""
from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.services.produto_service import ProdutoService
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.sqlalchemy_produto_repository import SQLAlchemyProdutoRepository


def get_produto_repository(
    db: Session = Depends(get_db),
) -> Generator[SQLAlchemyProdutoRepository, None, None]:
    """
    Factory para repositório de produtos.

    Cria uma instância do repositório SQLAlchemy por request.
    """
    yield SQLAlchemyProdutoRepository(db)


def get_produto_service(
    repo: SQLAlchemyProdutoRepository = Depends(get_produto_repository),
) -> Generator[ProdutoService, None, None]:
    """
    Factory para serviço de produtos.

    Injeta o repositório no service (Inversão de Dependência).
    O service não conhece a implementação concreta do repositório,
    apenas a interface (Protocol).
    """
    yield ProdutoService(repo)