"""
Exceções de domínio.
"""
from app.domain.exceptions.domain_exceptions import (
    DomainException,
    EntidadeNaoEncontrada,
    RegraDeNegocioViolada,
    EstoqueInsuficiente,
    DadosInvalidos,
)

__all__ = [
    "DomainException",
    "EntidadeNaoEncontrada",
    "RegraDeNegocioViolada",
    "EstoqueInsuficiente",
    "DadosInvalidos",
]