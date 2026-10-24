"""
Testes unitários do Service da camada Application.

Testa a lógica de negócio (use cases) com repository mockado.
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock

from app.application.dto.produto_dto import ProdutoCreateDTO, ProdutoUpdateDTO
from app.application.services.produto_service import ProdutoService
from app.domain.entities.produto import Produto
from app.domain.exceptions import (
    EntidadeNaoEncontrada,
    RegraDeNegocioViolada,
)
from app.domain.repositories.produto_repository import ProdutoRepository


class TestProdutoService:
    """Testes do ProdutoService."""

    @pytest.fixture
    def mock_repository(self):
        """Mock do repository."""
        return Mock(spec=ProdutoRepository)

    @pytest.fixture
    def service(self, mock_repository):
        """Service com repository mockado."""
        return ProdutoService(repository=mock_repository)

    @pytest.fixture
    def sample_produto(self):
        """Produto de exemplo."""
        return Produto(id=1, nome="Teclado", preco=Decimal("150.00"), estoque=10)

    # ===== CRIAÇÃO =====

    def test_criar_produto_sucesso(self, service, mock_repository):
        """Deve criar produto com sucesso."""
        create_dto = ProdutoCreateDTO(nome="Mouse", preco=Decimal("80.00"), estoque=5)
        mock_repository.criar.return_value = Produto(id=1, nome="Mouse", preco=Decimal("80.00"), estoque=5)

        result = service.criar_produto(create_dto)

        assert result.id == 1
        assert result.nome == "Mouse"
        assert result.preco == Decimal("80.00")
        assert result.estoque == 5
        mock_repository.criar.assert_called_once()

    def test_criar_produto_dados_invalidos_lanca_erro(self, service, mock_repository):
        """Deve lançar ValidationError para dados inválidos (validação no DTO)."""
        # Nome muito curto falha na criação do DTO
        with pytest.raises(Exception):  # ValidationError
            ProdutoCreateDTO(nome="A", preco=Decimal("10.00"))

    def test_criar_produto_repository_lanca_erro(self, service, mock_repository):
        """Deve propagar erro do repository."""
        create_dto = ProdutoCreateDTO(nome="Mouse", preco=Decimal("80.00"))
        mock_repository.criar.side_effect = Exception("DB Error")

        with pytest.raises(Exception, match="DB Error"):
            service.criar_produto(create_dto)

    # ===== BUSCA POR ID =====

    def test_buscar_produto_encontrado(self, service, mock_repository, sample_produto):
        """Deve buscar produto por ID quando existe."""
        mock_repository.buscar_por_id.return_value = sample_produto

        result = service.buscar_produto(1)

        assert result.id == 1
        assert result.nome == "Teclado"
        mock_repository.buscar_por_id.assert_called_once_with(1)

    def test_buscar_produto_nao_encontrado_lanca_erro(self, service, mock_repository):
        """Deve lançar EntidadeNaoEncontrada quando produto não existe."""
        mock_repository.buscar_por_id.return_value = None

        with pytest.raises(EntidadeNaoEncontrada) as exc_info:
            service.buscar_produto(999)

        assert exc_info.value.entidade == "Produto"
        assert exc_info.value.identificador == 999

    # ===== LISTAGEM =====

    def test_listar_produtos(self, service, mock_repository):
        """Deve listar todos os produtos."""
        produtos = [
            Produto(id=1, nome="Teclado", preco=Decimal("10"), estoque=1),
            Produto(id=2, nome="Mouse", preco=Decimal("20"), estoque=2),
        ]
        mock_repository.listar_todos.return_value = produtos

        result = service.listar_produtos()

        assert len(result) == 2
        assert result[0].nome == "Teclado"
        assert result[1].nome == "Mouse"
        mock_repository.listar_todos.assert_called_once()

    def test_listar_produtos_vazio(self, service, mock_repository):
        """Deve retornar lista vazia quando não há produtos."""
        mock_repository.listar_todos.return_value = []

        result = service.listar_produtos()

        assert result == []

    # ===== ATUALIZAÇÃO =====

    def test_atualizar_produto_sucesso(self, service, mock_repository, sample_produto):
        """Deve atualizar produto com sucesso."""
        mock_repository.buscar_por_id.return_value = sample_produto
        mock_repository.atualizar.return_value = sample_produto
        update_dto = ProdutoUpdateDTO(nome="Teclado Novo", preco=Decimal("200.00"))

        result = service.atualizar_produto(1, update_dto)

        assert result.nome == "Teclado Novo"
        assert result.preco == Decimal("200.00")
        mock_repository.buscar_por_id.assert_called_once_with(1)
        mock_repository.atualizar.assert_called_once()

    def test_atualizar_produto_nao_encontrado(self, service, mock_repository):
        """Deve lançar erro se produto não existe."""
        mock_repository.buscar_por_id.return_value = None
        update_dto = ProdutoUpdateDTO(nome="Novo")

        with pytest.raises(EntidadeNaoEncontrada):
            service.atualizar_produto(999, update_dto)

    def test_atualizar_apenas_nome(self, service, mock_repository, sample_produto):
        """Deve atualizar apenas o nome quando só nome é fornecido."""
        mock_repository.buscar_por_id.return_value = sample_produto
        mock_repository.atualizar.return_value = sample_produto
        update_dto = ProdutoUpdateDTO(nome="Novo Nome")

        result = service.atualizar_produto(1, update_dto)

        assert result.nome == "Novo Nome"
        assert result.preco == Decimal("150.00")  # Não mudou
        assert result.estoque == 10  # Não mudou

    def test_atualizar_preco_invalido_lanca_erro(self, service, mock_repository, sample_produto):
        """Deve lançar erro se preço for inválido (validação no DTO)."""
        mock_repository.buscar_por_id.return_value = sample_produto

        # Preço inválido falha na criação do DTO
        with pytest.raises(Exception):  # ValidationError
            ProdutoUpdateDTO(preco=Decimal("0"))

    # ===== EXCLUSÃO =====

    def test_remover_produto_sucesso(self, service, mock_repository, sample_produto):
        """Deve remover produto com sucesso."""
        mock_repository.remover.return_value = True

        service.remover_produto(1)

        mock_repository.remover.assert_called_once_with(1)

    def test_remover_produto_nao_encontrado(self, service, mock_repository):
        """Deve lançar erro se produto não existe."""
        mock_repository.buscar_por_id.return_value = None
        mock_repository.remover.return_value = False

        with pytest.raises(EntidadeNaoEncontrada):
            service.remover_produto(999)

    # ===== VERIFICAÇÃO DE EXISTÊNCIA =====

    def test_verificar_existencia_true(self, service, mock_repository):
        """Deve retornar True quando produto existe."""
        mock_repository.existe_por_id.return_value = True

        result = service._repository.existe_por_id(1)

        assert result is True

    def test_verificar_existencia_false(self, service, mock_repository):
        """Deve retornar False quando produto não existe."""
        mock_repository.existe_por_id.return_value = False

        result = service._repository.existe_por_id(999)

        assert result is False