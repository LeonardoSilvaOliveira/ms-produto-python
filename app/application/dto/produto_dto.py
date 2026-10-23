"""
DTOs (Data Transfer Objects) da camada de Aplicação.

Diferente dos schemas da API (presentation), estes são usados internamente
entre use cases/services e repositories. Focam na estrutura de dados
para lógica de negócio, não para serialização HTTP.
"""
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ProdutoDTO(BaseModel):
    """DTO base para produto - usado internamente."""
    id: Optional[int] = None
    nome: str = Field(min_length=2, max_length=100)
    preco: Decimal = Field(gt=0, decimal_places=2)
    estoque: int = Field(default=0, ge=0)

    model_config = ConfigDict(from_attributes=True)


class ProdutoCreateDTO(BaseModel):
    """DTO para criação de produto."""
    nome: str = Field(min_length=2, max_length=100)
    preco: Decimal = Field(gt=0, decimal_places=2)
    estoque: int = Field(default=0, ge=0)

    def to_entity(self) -> "Produto":
        """Converte para entidade de domínio."""
        from app.domain.entities.produto import Produto
        return Produto.criar(
            nome=self.nome,
            preco=self.preco,
            estoque=self.estoque,
        )


class ProdutoUpdateDTO(BaseModel):
    """DTO para atualização de produto (campos opcionais)."""
    nome: Optional[str] = Field(default=None, min_length=2, max_length=100)
    preco: Optional[Decimal] = Field(default=None, gt=0, decimal_places=2)
    estoque: Optional[int] = Field(default=None, ge=0)

    def aplicar_na_entity(self, entity: "Produto") -> None:
        """Aplica mudanças na entidade (apenas campos não-None)."""
        if self.nome is not None:
            entity.atualizar_nome(self.nome)
        if self.preco is not None:
            entity.atualizar_preco(self.preco)
        if self.estoque is not None:
            entity.estoque = self.estoque


class ProdutoResponseDTO(BaseModel):
    """DTO para resposta de produto."""
    id: int
    nome: str
    preco: Decimal
    estoque: int

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, entity: "Produto") -> "ProdutoResponseDTO":
        """Cria DTO a partir de entidade de domínio."""
        return cls(
            id=entity.id,
            nome=entity.nome,
            preco=entity.preco,
            estoque=entity.estoque,
        )


# Type aliases para facilitar uso
ProdutoListDTO = list[ProdutoResponseDTO]