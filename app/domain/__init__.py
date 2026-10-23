"""
Camada de Domínio - Regras de negócio puras.

Contém:
- Entidades (domain entities)
- Repositories (interfaces/protocols)
- Exceptions (domain exceptions)
"""
from app.domain.entities import Produto
from app.domain.repositories import ProdutoRepository
from app.domain.exceptions import (
    DomainException,
    EntidadeNaoEncontrada,
    RegraDeNegocioViolada,
    EstoqueInsuficiente,
    DadosInvalidos,
)

__all__ = [
    "Produto",
    "ProdutoRepository",
    "DomainException",
    "EntidadeNaoEncontrada",
    "RegraDeNegocioViolada",
    "EstoqueInsuficiente",
    "DadosInvalidos",
]