"""
Entidade de domínio - Produto.

Entidade pura de domínio, sem dependências de framework (SQLAlchemy, Pydantic, etc.).
Representa as regras de negócio centrais da aplicação.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(slots=True)
class Produto:
    """
    Entidade Produto do domínio.

    Attributes:
        id: Identificador único (None para novos produtos)
        nome: Nome do produto (2-100 caracteres)
        preco: Preço em Decimal (precisão monetária)
        estoque: Quantidade em estoque (>= 0)
    """
    id: Optional[int] = None
    nome: str = ""
    preco: Decimal = Decimal("0.00")
    estoque: int = 0

    def __post_init__(self):
        """Validações de domínio após inicialização."""
        if self.nome:
            self.nome = self.nome.strip()
            if len(self.nome) < 2:
                raise ValueError("Nome deve ter pelo menos 2 caracteres")
            if len(self.nome) > 100:
                raise ValueError("Nome deve ter no máximo 100 caracteres")
        if self.preco is not None and not isinstance(self.preco, Decimal):
            self.preco = Decimal(str(self.preco))
        if self.estoque is not None and self.estoque < 0:
            self.estoque = 0
        if self.preco is not None and self.preco <= 0:
            raise ValueError("Preço deve ser maior que zero")

    # Regras de negócio (domain logic)

    def pode_vender(self, quantidade: int) -> bool:
        """Verifica se há estoque suficiente para vender."""
        return self.estoque >= quantidade

    def reduzir_estoque(self, quantidade: int) -> None:
        """Reduz o estoque (lança exceção se insuficiente)."""
        if not self.pode_vender(quantidade):
            raise ValueError(f"Estoque insuficiente: {self.estoque} < {quantidade}")
        self.estoque -= quantidade

    def aumentar_estoque(self, quantidade: int) -> None:
        """Aumenta o estoque."""
        if quantidade < 0:
            raise ValueError("Quantidade deve ser positiva")
        self.estoque += quantidade

    def atualizar_preco(self, novo_preco: Decimal) -> None:
        """Atualiza o preço com validação."""
        if novo_preco <= 0:
            raise ValueError("Preço deve ser maior que zero")
        self.preco = novo_preco

    def atualizar_nome(self, novo_nome: str) -> None:
        """Atualiza o nome com validação."""
        nome_limpo = novo_nome.strip()
        if len(nome_limpo) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        if len(nome_limpo) > 100:
            raise ValueError("Nome deve ter no máximo 100 caracteres")
        self.nome = nome_limpo

    def to_dict(self) -> dict:
        """Converte para dicionário (útil para serialização)."""
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": float(self.preco),
            "estoque": self.estoque,
        }

    @classmethod
    def criar(cls, nome: str, preco: Decimal, estoque: int = 0) -> "Produto":
        """Factory method para criar novo produto válido."""
        produto = cls(nome=nome, preco=preco, estoque=estoque)
        # Validações já ocorrem no __post_init__
        return produto