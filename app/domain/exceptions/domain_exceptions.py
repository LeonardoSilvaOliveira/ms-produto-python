"""
Exceções de domínio.

Exceções personalizadas que representam erros de regras de negócio.
Podem ser capturadas na camada de apresentação e convertidas em respostas HTTP apropriadas.
"""


class DomainException(Exception):
    """Exceção base de domínio."""

    def __init__(self, message: str, code: str = "DOMAIN_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class EntidadeNaoEncontrada(DomainException):
    """Lançada quando uma entidade não é encontrada."""

    def __init__(self, entidade: str, identificador: str | int):
        super().__init__(
            f"{entidade} não encontrado(a): {identificador}",
            code="NOT_FOUND",
        )
        self.entidade = entidade
        self.identificador = identificador


class RegraDeNegocioViolada(DomainException):
    """Lançada quando uma regra de negócio é violada."""

    def __init__(self, message: str):
        super().__init__(message, code="BUSINESS_RULE_VIOLATION")


class EstoqueInsuficiente(RegraDeNegocioViolada):
    """Lançada quando não há estoque suficiente para uma operação."""

    def __init__(self, disponivel: int, solicitado: int):
        super().__init__(
            f"Estoque insuficiente: disponível {disponivel}, solicitado {solicitado}"
        )
        self.disponivel = disponivel
        self.solicitado = solicitado


class DadosInvalidos(DomainException):
    """Lançada quando dados de entrada são inválidos."""

    def __init__(self, campo: str, message: str):
        super().__init__(f"Campo '{campo}': {message}", code="INVALID_DATA")
        self.campo = campo