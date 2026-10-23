"""
Schemas Pydantic para a API (Camada de Apresentação).

Define contratos de request/response HTTP.
Diferente dos DTOs da aplicação, estes focam em validação e serialização HTTP.
"""
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ProdutoCreateRequest(BaseModel):
    """Request para criar produto."""
    nome: str = Field(min_length=2, max_length=100, examples=["Teclado Mecânico"])
    preco: Decimal = Field(gt=0, decimal_places=2, examples=[150.00])
    estoque: int = Field(default=0, ge=0, examples=[10])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "Teclado Mecânico",
                "preco": "150.00",
                "estoque": 10
            }
        }
    )


class ProdutoUpdateRequest(BaseModel):
    """Request para atualizar produto (campos opcionais)."""
    nome: Optional[str] = Field(default=None, min_length=2, max_length=100)
    preco: Optional[Decimal] = Field(default=None, gt=0, decimal_places=2)
    estoque: Optional[int] = Field(default=None, ge=0)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "Teclado Mecânico RGB",
                "preco": "180.00"
            }
        }
    )


class ProdutoResponse(BaseModel):
    """Response de produto."""
    id: int
    nome: str
    preco: Decimal
    estoque: int

    model_config = ConfigDict(from_attributes=True)


class ProdutoListResponse(BaseModel):
    """Response para listagem paginada (futuro)."""
    items: list[ProdutoResponse]
    total: int
    page: int
    size: int


class MessageResponse(BaseModel):
    """Response genérica de mensagem."""
    message: str


class ErrorResponse(BaseModel):
    """Response de erro padronizada."""
    detail: str
    code: Optional[str] = None