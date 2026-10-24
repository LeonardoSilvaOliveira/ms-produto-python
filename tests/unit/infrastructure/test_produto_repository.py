"""
Testes de integração do Repository (Infraestrutura).

Testa o repository real contra banco de dados (SQLite em memória).
"""
import pytest
from decimal import Decimal

from app.domain.entities.produto import Produto
from app.infrastructure.repositories.sqlalchemy_produto_repository import SQLAlchemyProdutoRepository
from app.infrastructure.models.produto_model import ProdutoModel


class TestSQLAlchemyProdutoRepository:
    """Testes do repository SQLAlchemy."""

    @pytest.fixture
    def repository(self, db_session):
        """Repository com session de teste."""
        return SQLAlchemyProdutoRepository(db_session)

    def test_criar_produto(self, repository, db_session):
        """Deve criar produto e retornar com ID."""
        produto = Produto(nome="Teclado", preco=Decimal("150.00"), estoque=10)

        resultado = repository.criar(produto)

        assert resultado.id is not None
        assert resultado.nome == "Teclado"
        assert resultado.preco == Decimal("150.00")
        assert resultado.estoque == 10

        # Verifica se foi persistido no banco
        db_produto = db_session.query(ProdutoModel).filter_by(id=resultado.id).first()
        assert db_produto is not None
        assert db_produto.nome == "Teclado"

    def test_buscar_por_id_encontrado(self, repository, db_session):
        """Deve buscar produto por ID quando existe."""
        # Cria produto no banco
        db_produto = ProdutoModel(nome="Mouse", preco=Decimal("80.00"), estoque=5)
        db_session.add(db_produto)
        db_session.flush()
        db_session.refresh(db_produto)

        resultado = repository.buscar_por_id(db_produto.id)

        assert resultado is not None
        assert resultado.id == db_produto.id
        assert resultado.nome == "Mouse"
        assert resultado.preco == Decimal("80.00")
        assert resultado.estoque == 5

    def test_buscar_por_id_nao_encontrado(self, repository):
        """Deve retornar None quando produto não existe."""
        resultado = repository.buscar_por_id(999)

        assert resultado is None

    def test_listar_todos(self, repository, db_session):
        """Deve listar todos os produtos."""
        produtos = [
            ProdutoModel(nome="Teclado", preco=Decimal("150.00"), estoque=10),
            ProdutoModel(nome="Mouse", preco=Decimal("80.00"), estoque=15),
            ProdutoModel(nome="Monitor", preco=Decimal("899.90"), estoque=5),
        ]
        db_session.add_all(produtos)
        db_session.flush()

        resultado = repository.listar_todos()

        assert len(resultado) == 3
        assert all(isinstance(p, Produto) for p in resultado)

    def test_listar_todos_vazio(self, repository):
        """Deve retornar lista vazia quando não há produtos."""
        resultado = repository.listar_todos()

        assert resultado == []

    def test_atualizar_produto(self, repository, db_session):
        """Deve atualizar produto existente."""
        # Cria produto
        db_produto = ProdutoModel(nome="Original", preco=Decimal("100.00"), estoque=10)
        db_session.add(db_produto)
        db_session.flush()
        db_session.refresh(db_produto)

        # Atualiza via entity
        produto = repository.buscar_por_id(db_produto.id)
        produto.atualizar_nome("Atualizado")
        produto.atualizar_preco(Decimal("200.00"))

        resultado = repository.atualizar(produto)

        assert resultado.nome == "Atualizado"
        assert resultado.preco == Decimal("200.00")
        assert resultado.estoque == 10

        # Verifica no banco
        db_atualizado = db_session.query(ProdutoModel).filter_by(id=db_produto.id).first()
        assert db_atualizado.nome == "Atualizado"
        assert db_atualizado.preco == Decimal("200.00")

    def test_remover_produto_existente(self, repository, db_session):
        """Deve remover produto existente e retornar True."""
        db_produto = ProdutoModel(nome="Para Remover", preco=Decimal("50.00"), estoque=3)
        db_session.add(db_produto)
        db_session.flush()
        db_session.refresh(db_produto)

        resultado = repository.remover(db_produto.id)

        assert resultado is True

        # Verifica se foi removido do banco
        db_removido = db_session.query(ProdutoModel).filter_by(id=db_produto.id).first()
        assert db_removido is None

    def test_remover_produto_inexistente(self, repository):
        """Deve retornar False ao tentar remover produto inexistente."""
        resultado = repository.remover(999)

        assert resultado is False

    def test_existe_por_id_true(self, repository, db_session):
        """Deve retornar True quando produto existe."""
        db_produto = ProdutoModel(nome="Existe", preco=Decimal("10.00"), estoque=1)
        db_session.add(db_produto)
        db_session.flush()
        db_session.refresh(db_produto)

        resultado = repository.existe_por_id(db_produto.id)

        assert resultado is True

    def test_existe_por_id_false(self, repository):
        """Deve retornar False quando produto não existe."""
        resultado = repository.existe_por_id(999)

        assert resultado is False