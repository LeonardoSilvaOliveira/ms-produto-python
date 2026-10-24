"""
Testes unitários da Entidade de Domínio - Produto.

Testa regras de negócio puras, sem dependências externas.
"""
from decimal import Decimal

import pytest

from app.domain.entities.produto import Produto
from app.domain.exceptions import (
    RegraDeNegocioViolada,
    EstoqueInsuficiente,
    DadosInvalidos,
)


class TestProdutoEntity:
    """Testes da entidade Produto."""

    def test_criar_produto_valido(self):
        """Deve criar produto com dados válidos."""
        produto = Produto.criar(
            nome="Teclado Mecânico",
            preco=Decimal("150.00"),
            estoque=10,
        )

        assert produto.nome == "Teclado Mecânico"
        assert produto.preco == Decimal("150.00")
        assert produto.estoque == 10
        assert produto.id is None  # ID é None antes de persistir

    def test_criar_produto_com_estoque_padrao_zero(self):
        """Deve criar produto com estoque 0 por padrão."""
        produto = Produto.criar(nome="Mouse", preco=Decimal("80.00"))

        assert produto.estoque == 0

    def test_criar_produto_nome_com_espacos(self):
        """Deve remover espaços extras do nome."""
        produto = Produto.criar(nome="  Teclado  ", preco=Decimal("100.00"))

        assert produto.nome == "Teclado"

    def test_criar_produto_preco_como_string(self):
        """Deve converter preço string para Decimal."""
        produto = Produto.criar(nome="Produto", preco="99.99")

        assert isinstance(produto.preco, Decimal)
        assert produto.preco == Decimal("99.99")


class TestProdutoValidacoes:
    """Testes de validações de domínio."""

    def test_nome_muito_curto_levanta_erro(self):
        """Nome com menos de 2 caracteres deve falhar."""
        with pytest.raises(ValueError, match="pelo menos 2 caracteres"):
            Produto.criar(nome="A", preco=Decimal("10.00"))

    def test_nome_muito_longo_levanta_erro(self):
        """Nome com mais de 100 caracteres deve falhar."""
        nome_longo = "A" * 101
        with pytest.raises(ValueError, match="no máximo 100 caracteres"):
            Produto.criar(nome=nome_longo, preco=Decimal("10.00"))

    def test_preco_zero_ou_negativo_levanta_erro(self):
        """Preço <= 0 deve falhar."""
        with pytest.raises(ValueError, match="maior que zero"):
            Produto.criar(nome="Produto", preco=Decimal("0"))

        with pytest.raises(ValueError, match="maior que zero"):
            Produto.criar(nome="Produto", preco=Decimal("-10.00"))

    def test_estoque_negativo_ajustado_para_zero(self):
        """Estoque negativo deve ser ajustado para 0 (no __post_init__)."""
        produto = Produto(nome="Produto", preco=Decimal("10.00"), estoque=-5)
        assert produto.estoque == 0


class TestProdutoRegrasDeNegocio:
    """Testes das regras de negócio (métodos da entidade)."""

    def test_pode_vender_com_estoque_suficiente(self):
        """Deve retornar True quando há estoque suficiente."""
        produto = Produto.criar(nome="Produto", preco=Decimal("10.00"), estoque=10)

        assert produto.pode_vender(5) is True
        assert produto.pode_vender(10) is True

    def test_pode_vender_sem_estoque_suficiente(self):
        """Deve retornar False quando não há estoque suficiente."""
        produto = Produto.criar(nome="Produto", preco=Decimal("10.00"), estoque=5)

        assert produto.pode_vender(6) is False
        assert produto.pode_vender(10) is False

    def test_reduzir_estoque_com_sucesso(self):
        """Deve reduzir estoque quando há quantidade suficiente."""
        produto = Produto.criar(nome="Produto", preco=Decimal("10.00"), estoque=10)

        produto.reduzir_estoque(3)

        assert produto.estoque == 7

    def test_reduzir_estoque_insuficiente_levanta_erro(self):
        """Deve levantar ValueError quando estoque insuficiente."""
        produto = Produto.criar(nome="Produto", preco=Decimal("10.00"), estoque=5)

        with pytest.raises(ValueError, match="Estoque insuficiente"):
            produto.reduzir_estoque(10)

    def test_aumentar_estoque_com_sucesso(self):
        """Deve aumentar estoque corretamente."""
        produto = Produto.criar(nome="Produto", preco=Decimal("10.00"), estoque=5)

        produto.aumentar_estoque(10)

        assert produto.estoque == 15

    def test_aumentar_estoque_negativo_levanta_erro(self):
        """Deve falhar ao tentar aumentar com valor negativo."""
        produto = Produto.criar(nome="Produto", preco=Decimal("10.00"), estoque=5)

        with pytest.raises(ValueError, match="positiva"):
            produto.aumentar_estoque(-1)

    def test_atualizar_preco_valido(self):
        """Deve atualizar preço com valor válido."""
        produto = Produto.criar(nome="Produto", preco=Decimal("10.00"))

        produto.atualizar_preco(Decimal("20.00"))

        assert produto.preco == Decimal("20.00")

    def test_atualizar_preco_invalido_levanta_erro(self):
        """Deve falhar ao atualizar com preço inválido."""
        produto = Produto.criar(nome="Produto", preco=Decimal("10.00"))

        with pytest.raises(ValueError, match="maior que zero"):
            produto.atualizar_preco(Decimal("0"))

    def test_atualizar_nome_valido(self):
        """Deve atualizar nome com valor válido."""
        produto = Produto.criar(nome="Produto Antigo", preco=Decimal("10.00"))

        produto.atualizar_nome("Novo Nome")

        assert produto.nome == "Novo Nome"

    def test_atualizar_nome_com_espacos(self):
        """Deve remover espaços ao atualizar nome."""
        produto = Produto.criar(nome="Produto", preco=Decimal("10.00"))

        produto.atualizar_nome("  Novo Nome  ")

        assert produto.nome == "Novo Nome"

    def test_atualizar_nome_muito_curto_levanta_erro(self):
        """Deve falhar ao atualizar com nome muito curto."""
        produto = Produto.criar(nome="Produto", preco=Decimal("10.00"))

        with pytest.raises(ValueError, match="pelo menos 2 caracteres"):
            produto.atualizar_nome("A")


class TestProdutoSerializacao:
    """Testes de serialização da entidade."""

    def test_to_dict_retorna_dados_corretos(self):
        """to_dict deve retornar dicionário com dados corretos."""
        produto = Produto(
            id=1,
            nome="Teclado",
            preco=Decimal("150.00"),
            estoque=10,
        )

        data = produto.to_dict()

        assert data == {
            "id": 1,
            "nome": "Teclado",
            "preco": 150.0,
            "estoque": 10,
        }

    def test_to_dict_sem_id(self):
        """to_dict deve incluir id como None quando não definido."""
        produto = Produto(nome="Teclado", preco=Decimal("150.00"), estoque=10)

        data = produto.to_dict()

        assert data["id"] is None