"""
Model SQLAlchemy para Produto (tabela do banco).

Representa a estrutura da tabela no banco de dados.
Fica na camada de infraestrutura (implementação concreta).
"""
from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ProdutoModel(Base):
    """
    Model SQLAlchemy para a tabela 'produtos'.

    Mapeamento objeto-relacional (ORM) da tabela.
    """
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    estoque: Mapped[int] = mapped_column(default=0, nullable=False)

    def __repr__(self) -> str:
        return f"<ProdutoModel(id={self.id}, nome='{self.nome}', preco={self.preco}, estoque={self.estoque})>"

    def to_entity(self) -> "Produto":
        """Converte model SQLAlchemy para entidade de domínio."""
        from app.domain.entities.produto import Produto
        return Produto(
            id=self.id,
            nome=self.nome,
            preco=self.preco,
            estoque=self.estoque,
        )

    @classmethod
    def from_entity(cls, entity: "Produto") -> "ProdutoModel":
        """Cria model a partir de entidade de domínio."""
        return cls(
            id=entity.id,
            nome=entity.nome,
            preco=entity.preco,
            estoque=entity.estoque,
        )

    def update_from_entity(self, entity: "Produto") -> None:
        """Atualiza model com dados da entidade."""
        self.nome = entity.nome
        self.preco = entity.preco
        self.estoque = entity.estoque