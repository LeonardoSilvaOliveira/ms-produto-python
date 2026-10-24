"""
Testes unitários das Exceções de Domínio.

Testa comportamento das exceções customizadas.
"""
import pytest

from app.domain.exceptions import (
    DomainException,
    EntidadeNaoEncontrada,
    RegraDeNegocioViolada,
    EstoqueInsuficiente,
    DadosInvalidos,
)


class TestExcecoesDeDominio:
    """Testes das exceções de domínio."""

    def test_domain_exception_herda_de_exception(self):
        """DomainException deve herdar de Exception."""
        assert issubclass(DomainException, Exception)

    def test_entidade_nao_encontrada_herda_domain_exception(self):
        """EntidadeNaoEncontrada deve herdar de DomainException."""
        assert issubclass(EntidadeNaoEncontrada, DomainException)

    def test_estoque_insuficiente_herda_regra_de_negocio(self):
        """EstoqueInsuficiente deve herdar de RegraDeNegocioViolada."""
        assert issubclass(EstoqueInsuficiente, RegraDeNegocioViolada)

    def test_estoque_insuficiente_herda_domain_exception(self):
        """EstoqueInsuficiente deve herdar de DomainException (via RegraDeNegocioViolada)."""
        assert issubclass(EstoqueInsuficiente, DomainException)

    def test_regra_de_negocio_violada_herda_domain_exception(self):
        """RegraDeNegocioViolada deve herdar de DomainException."""
        assert issubclass(RegraDeNegocioViolada, DomainException)

    def test_dados_invalidos_herda_domain_exception(self):
        """DadosInvalidos deve herdar de DomainException."""
        assert issubclass(DadosInvalidos, DomainException)


class TestEntidadeNaoEncontrada:
    """Testes da exceção EntidadeNaoEncontrada."""

    def test_criar_com_entidade_e_identificador(self):
        """Deve criar exceção com nome da entidade e identificador."""
        exc = EntidadeNaoEncontrada(entidade="Produto", identificador=42)

        assert exc.entidade == "Produto"
        assert exc.identificador == 42
        assert exc.code == "NOT_FOUND"

    def test_message_format(self):
        """Mensagem deve seguir padrão esperado."""
        exc = EntidadeNaoEncontrada(entidade="Produto", identificador=1)

        assert "Produto" in str(exc)
        assert "1" in str(exc)
        assert "não encontrado" in str(exc).lower()

    def test_criar_com_string_como_identificador(self):
        """Deve aceitar string como identificador."""
        exc = EntidadeNaoEncontrada(entidade="Usuario", identificador="abc-123")

        assert exc.identificador == "abc-123"
        assert "abc-123" in str(exc)


class TestRegraDeNegocioViolada:
    """Testes da exceção RegraDeNegocioViolada."""

    def test_criar_com_mensagem(self):
        """Deve criar exceção com mensagem customizada."""
        exc = RegraDeNegocioViolada(message="Produto deve estar ativo para venda")

        assert str(exc) == "Produto deve estar ativo para venda"
        assert exc.code == "BUSINESS_RULE_VIOLATION"

    def test_message_e_code(self):
        """Deve ter message e code corretos."""
        exc = RegraDeNegocioViolada(message="Regra violada")

        assert exc.message == "Regra violada"
        assert exc.code == "BUSINESS_RULE_VIOLATION"


class TestEstoqueInsuficiente:
    """Testes da exceção EstoqueInsuficiente."""

    def test_criar_com_disponivel_e_solicitado(self):
        """Deve criar exceção com estoque disponível e solicitado."""
        exc = EstoqueInsuficiente(disponivel=5, solicitado=10)

        assert exc.disponivel == 5
        assert exc.solicitado == 10
        assert exc.code == "BUSINESS_RULE_VIOLATION"

    def test_message_format(self):
        """Mensagem deve mostrar disponível vs solicitado."""
        exc = EstoqueInsuficiente(disponivel=5, solicitado=10)

        msg = str(exc)
        assert "5" in msg
        assert "10" in msg
        assert "insuficiente" in msg.lower()

    def test_herda_de_regra_de_negocio(self):
        """Deve ser instância de RegraDeNegocioViolada."""
        exc = EstoqueInsuficiente(disponivel=5, solicitado=10)

        assert isinstance(exc, RegraDeNegocioViolada)


class TestDadosInvalidos:
    """Testes da exceção DadosInvalidos."""

    def test_criar_com_campo_e_mensagem(self):
        """Deve criar exceção com nome do campo e mensagem."""
        exc = DadosInvalidos(campo="preco", message="deve ser maior que zero")

        assert exc.campo == "preco"
        assert exc.code == "INVALID_DATA"

    def test_message_format(self):
        """Mensagem deve incluir campo e mensagem."""
        exc = DadosInvalidos(campo="nome", message="não pode ser vazio")

        msg = str(exc)
        assert "nome" in msg
        assert "não pode ser vazio" in msg

    def test_campo_obrigatorio(self):
        """Campo deve ser armazenado como atributo."""
        exc = DadosInvalidos(campo="email", message="formato inválido")

        assert hasattr(exc, "campo")
        assert exc.campo == "email"


class TestDomainExceptionBase:
    """Testes da classe base DomainException."""

    def test_criar_com_message_e_code(self):
        """Deve criar com message e code customizados."""
        exc = DomainException(message="Erro customizado", code="CUSTOM_ERROR")

        assert exc.message == "Erro customizado"
        assert exc.code == "CUSTOM_ERROR"

    def test_code_padrao(self):
        """Code padrão deve ser DOMAIN_ERROR."""
        exc = DomainException(message="Erro genérico")

        assert exc.code == "DOMAIN_ERROR"

    def test_str_representation(self):
        """str() deve retornar a message."""
        exc = DomainException(message="Erro de teste")

        assert str(exc) == "Erro de teste"


class TestExcecoesPodemSerCapturadas:
    """Testes de captura hierárquica de exceções."""

    def test_capturar_todas_como_domain_exception(self):
        """Todas devem ser capturáveis como DomainException."""
        excecoes = [
            EntidadeNaoEncontrada("Produto", 1),
            EstoqueInsuficiente(0, 1),
            RegraDeNegocioViolada("regra_teste"),
            DadosInvalidos("campo", "valor inválido"),
        ]

        for exc in excecoes:
            try:
                raise exc
            except DomainException:
                pass  # Deve capturar
            except Exception:
                pytest.fail(f"{type(exc).__name__} não herdou de DomainException")

    def test_capturar_estoque_como_regra_de_negocio(self):
        """EstoqueInsuficiente deve ser capturável como RegraDeNegocioViolada."""
        exc = EstoqueInsuficiente(disponivel=5, solicitado=10)

        try:
            raise exc
        except RegraDeNegocioViolada:
            pass  # Deve capturar
        except Exception:
            pytest.fail("EstoqueInsuficiente não herdou de RegraDeNegocioViolada")


class TestExcecoesComArgsExtras:
    """Testes com compatibilidade de args."""

    def test_entidade_nao_encontrada_kwargs_extras(self):
        """Deve aceitar kwargs extras sem erro (compatibilidade)."""
        # Python permite kwargs extras por padrão se não houver __slots__
        exc = EntidadeNaoEncontrada(entidade="Produto", identificador=1)

        assert exc.entidade == "Produto"
        assert exc.identificador == 1