"""
Serviço de Aplicação (Use Case) para Produtos.

Orquestra as operações de negócio, coordenando repositórios e entidades.
Não conhece detalhes de HTTP, banco de dados ou frameworks externos.
"""
from decimal import Decimal
from typing import Sequence

from app.domain.entities.produto import Produto
from app.domain.repositories.produto_repository import ProdutoRepository
from app.domain.exceptions import (
    EntidadeNaoEncontrada,
    RegraDeNegocioViolada,
    DadosInvalidos,
)
from app.application.dto.produto_dto import (
    ProdutoCreateDTO,
    ProdutoUpdateDTO,
    ProdutoResponseDTO,
)


class ProdutoService:
    """
    Serviço de aplicação para gerenciamento de produtos.

    Implementa os casos de uso (use cases) relacionados a produtos.
    Recebe repository via injeção de dependência (inversão de controle).
    """

    def __init__(self, repository: ProdutoRepository):
        self._repository = repository

    # Casos de uso (Use Cases)

    def criar_produto(self, dto: ProdutoCreateDTO) -> ProdutoResponseDTO:
        """
        Caso de uso: Criar novo produto.

        Args:
            dto: Dados para criação

        Returns:
            DTO do produto criado

        Raises:
            RegraDeNegocioViolada: Se dados inválidos
        """
        try:
            entity = dto.to_entity()
        except ValueError as e:
            raise RegraDeNegocioViolada(str(e))

        produto_criado = self._repository.criar(entity)
        return ProdutoResponseDTO.from_entity(produto_criado)

    def buscar_produto(self, produto_id: int) -> ProdutoResponseDTO:
        """
        Caso de uso: Buscar produto por ID.

        Args:
            produto_id: ID do produto

        Returns:
            DTO do produto encontrado

        Raises:
            EntidadeNaoEncontrada: Se produto não existe
        """
        produto = self._repository.buscar_por_id(produto_id)
        if produto is None:
            raise EntidadeNaoEncontrada("Produto", produto_id)
        return ProdutoResponseDTO.from_entity(produto)

    def listar_produtos(self) -> list[ProdutoResponseDTO]:
        """
        Caso de uso: Listar todos os produtos.

        Returns:
            Lista de DTOs de produtos
        """
        produtos = self._repository.listar_todos()
        return [ProdutoResponseDTO.from_entity(p) for p in produtos]

    def atualizar_produto(self, produto_id: int, dto: ProdutoUpdateDTO) -> ProdutoResponseDTO:
        """
        Caso de uso: Atualizar produto existente.

        Args:
            produto_id: ID do produto
            dto: Dados para atualização (campos opcionais)

        Returns:
            DTO do produto atualizado

        Raises:
            EntidadeNaoEncontrada: Se produto não existe
            RegraDeNegocioViolada: Se dados inválidos
        """
        # Verifica se existe
        produto = self._repository.buscar_por_id(produto_id)
        if produto is None:
            raise EntidadeNaoEncontrada("Produto", produto_id)

        # Aplica mudanças
        try:
            dto.aplicar_na_entity(produto)
        except ValueError as e:
            raise RegraDeNegocioViolada(str(e))

        # Persiste
        produto_atualizado = self._repository.atualizar(produto)
        return ProdutoResponseDTO.from_entity(produto_atualizado)

    def remover_produto(self, produto_id: int) -> None:
        """
        Caso de uso: Remover produto.

        Args:
            produto_id: ID do produto

        Raises:
            EntidadeNaoEncontrada: Se produto não existe
        """
        removido = self._repository.remover(produto_id)
        if not removido:
            raise EntidadeNaoEncontrada("Produto", produto_id)