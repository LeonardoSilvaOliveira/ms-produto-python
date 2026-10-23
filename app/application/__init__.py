"""
Camada de Aplicação - Casos de uso (Use Cases) e DTOs.

Orquestra a lógica de negócio coordenando repositórios e entidades.
Não conhece detalhes de HTTP, banco de dados ou frameworks externos.
"""
from app.application.dto import (
    ProdutoDTO,
    ProdutoCreateDTO,
    ProdutoUpdateDTO,
    ProdutoResponseDTO,
    ProdutoListDTO,
)
from app.application.services import ProdutoService

__all__ = [
    "ProdutoDTO",
    "ProdutoCreateDTO",
    "ProdutoUpdateDTO",
    "ProdutoResponseDTO",
    "ProdutoListDTO",
    "ProdutoService",
]