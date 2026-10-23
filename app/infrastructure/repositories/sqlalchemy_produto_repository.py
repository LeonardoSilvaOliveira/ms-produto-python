"""
Implementação concreta do repositório usando SQLAlchemy.

Implementa o Protocol ProdutoRepository definido no domínio.
Faz a conversão entre Models SQLAlchemy e Entidades de Domínio.
"""
from typing import Sequence, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.produto import Produto
from app.domain.repositories.produto_repository import ProdutoRepository
from app.infrastructure.models.produto_model import ProdutoModel


class SQLAlchemyProdutoRepository(ProdutoRepository):
    """
    Repositório de produtos usando SQLAlchemy.

    Implementa a interface ProdutoRepository (Protocol).
    """

    def __init__(self, session: Session):
        self._session = session

    def criar(self, produto: Produto) -> Produto:
        """Cria novo produto no banco."""
        model = ProdutoModel.from_entity(produto)
        self._session.add(model)
        self._session.flush()  # Gera ID sem commit
        self._session.refresh(model)
        return model.to_entity()

    def buscar_por_id(self, produto_id: int) -> Optional[Produto]:
        """Busca produto por ID."""
        model = self._session.get(ProdutoModel, produto_id)
        if model is None:
            return None
        return model.to_entity()

    def listar_todos(self) -> Sequence[Produto]:
        """Lista todos os produtos ordenados por ID."""
        stmt = select(ProdutoModel).order_by(ProdutoModel.id)
        models = self._session.scalars(stmt).all()
        return [model.to_entity() for model in models]

    def atualizar(self, produto: Produto) -> Produto:
        """Atualiza produto existente."""
        model = self._session.get(ProdutoModel, produto.id)
        if model is None:
            # Não deve acontecer se service verificou antes
            raise ValueError(f"Produto {produto.id} não encontrado para atualização")

        model.update_from_entity(produto)
        self._session.flush()
        self._session.refresh(model)
        return model.to_entity()

    def remover(self, produto_id: int) -> bool:
        """Remove produto por ID."""
        model = self._session.get(ProdutoModel, produto_id)
        if model is None:
            return False
        self._session.delete(model)
        self._session.flush()
        return True

    def existe_por_id(self, produto_id: int) -> bool:
        """Verifica se produto existe por ID."""
        return self._session.get(ProdutoModel, produto_id) is not None