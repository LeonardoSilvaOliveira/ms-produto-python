"""
Interface (Protocol) do Repositório de Produtos.

Define o contrato que toda implementação de repositório deve seguir.
Usa typing.Protocol para duck typing estático (similar a Interface do Java).
"""
from typing import Protocol, Sequence, Optional

from app.domain.entities.produto import Produto


class ProdutoRepository(Protocol):
    """
    Protocol para repositório de produtos.

    Qualquer classe que implemente esses métodos é compatível.
    Isso permite injeção de dependência e testes com mocks.
    """

    def criar(self, produto: Produto) -> Produto:
        """
        Cria um novo produto.

        Args:
            produto: Entidade Produto (sem ID)

        Returns:
            Produto com ID preenchido
        """
        ...

    def buscar_por_id(self, produto_id: int) -> Optional[Produto]:
        """
        Busca produto por ID.

        Args:
            produto_id: ID do produto

        Returns:
            Produto se encontrado, None caso contrário
        """
        ...

    def listar_todos(self) -> Sequence[Produto]:
        """
        Lista todos os produtos.

        Returns:
            Sequência de produtos
        """
        ...

    def atualizar(self, produto: Produto) -> Produto:
        """
        Atualiza um produto existente.

        Args:
            produto: Entidade com ID e dados atualizados

        Returns:
            Produto atualizado
        """
        ...

    def remover(self, produto_id: int) -> bool:
        """
        Remove um produto por ID.

        Args:
            produto_id: ID do produto a remover

        Returns:
            True se removido, False se não encontrado
        """
        ...

    def existe_por_id(self, produto_id: int) -> bool:
        """
        Verifica se produto existe por ID.

        Args:
            produto_id: ID do produto

        Returns:
            True se existe, False caso contrário
        """
        ...