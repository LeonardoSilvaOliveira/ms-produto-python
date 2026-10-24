"""
Testes unitários dos DTOs da camada Application.

Testa validação e conversão de dados de entrada/saída.
"""
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.application.dto.produto_dto import (
    ProdutoCreateDTO,
    ProdutoUpdateDTO,
    ProdutoResponseDTO,
)


class TestProdutoCreateDTO:
    """Testes do DTO de criação de produto."""

    def test_criar_com_dados_validos(self):
        """Deve criar DTO com dados válidos."""
        dto = ProdutoCreateDTO(nome="Teclado Mecânico", preco=Decimal("150.00"), estoque=10)

        assert dto.nome == "Teclado Mecânico"
        assert dto.preco == Decimal("150.00")
        assert dto.estoque == 10

    def test_criar_com_estoque_padrao_zero(self):
        """Estoque deve ser 0 por padrão."""
        dto = ProdutoCreateDTO(nome="Mouse", preco=Decimal("80.00"))

        assert dto.estoque == 0

    def test_criar_com_preco_como_string(self):
        """Deve converter string para Decimal."""
        dto = ProdutoCreateDTO(nome="Produto", preco="99.99")

        assert isinstance(dto.preco, Decimal)
        assert dto.preco == Decimal("99.99")

    def test_criar_com_preco_como_float(self):
        """Deve converter float para Decimal."""
        dto = ProdutoCreateDTO(nome="Produto", preco=49.99)

        assert isinstance(dto.preco, Decimal)
        assert dto.preco == Decimal("49.99")

    def test_nome_nao_e_limpo_no_dto(self):
        """DTO não limpa espaços - a entidade faz isso no to_entity()."""
        dto = ProdutoCreateDTO(nome="  Teclado  ", preco=Decimal("100.00"))

        # DTO mantém os espaços; a entidade limpa no to_entity()
        assert dto.nome == "  Teclado  "

    def test_to_entity_limpa_espacos(self):
        """to_entity deve converter e limpar espaços via entidade."""
        dto = ProdutoCreateDTO(nome="  Teclado  ", preco=Decimal("100.00"))

        entity = dto.to_entity()

        assert entity.nome == "Teclado"

    def test_nome_muito_curto_falha(self):
        """Nome com menos de 2 caracteres deve falhar."""
        with pytest.raises(ValidationError) as exc_info:
            ProdutoCreateDTO(nome="A", preco=Decimal("10.00"))

        errors = exc_info.value.errors()
        assert any("min_length" in str(e) or "2" in str(e) for e in errors)

    def test_nome_muito_longo_falha(self):
        """Nome com mais de 100 caracteres deve falhar."""
        nome_longo = "A" * 101
        with pytest.raises(ValidationError):
            ProdutoCreateDTO(nome=nome_longo, preco=Decimal("10.00"))

    def test_preco_zero_ou_negativo_falha(self):
        """Preço <= 0 deve falhar."""
        with pytest.raises(ValidationError):
            ProdutoCreateDTO(nome="Produto", preco=Decimal("0"))

        with pytest.raises(ValidationError):
            ProdutoCreateDTO(nome="Produto", preco=Decimal("-10.00"))

    def test_estoque_negativo_falha(self):
        """Estoque negativo deve falhar."""
        with pytest.raises(ValidationError):
            ProdutoCreateDTO(nome="Produto", preco=Decimal("10.00"), estoque=-1)

    def test_campos_obrigatorios(self):
        """nome e preco são obrigatórios."""
        with pytest.raises(ValidationError) as exc_info:
            ProdutoCreateDTO()

        errors = exc_info.value.errors()
        field_names = [e["loc"][0] for e in errors]
        assert "nome" in field_names
        assert "preco" in field_names


class TestProdutoUpdateDTO:
    """Testes do DTO de atualização de produto."""

    def test_atualizar_apenas_nome(self):
        """Deve permitir atualizar apenas o nome."""
        dto = ProdutoUpdateDTO(nome="Novo Nome")

        assert dto.nome == "Novo Nome"
        assert dto.preco is None
        assert dto.estoque is None

    def test_atualizar_apenas_preco(self):
        """Deve permitir atualizar apenas o preço."""
        dto = ProdutoUpdateDTO(preco=Decimal("200.00"))

        assert dto.preco == Decimal("200.00")
        assert dto.nome is None
        assert dto.estoque is None

    def test_atualizar_apenas_estoque(self):
        """Deve permitir atualizar apenas o estoque."""
        dto = ProdutoUpdateDTO(estoque=20)

        assert dto.estoque == 20
        assert dto.nome is None
        assert dto.preco is None

    def test_atualizar_todos_campos(self):
        """Deve permitir atualizar todos os campos."""
        dto = ProdutoUpdateDTO(nome="Novo", preco=Decimal("150.00"), estoque=5)

        assert dto.nome == "Novo"
        assert dto.preco == Decimal("150.00")
        assert dto.estoque == 5

    def test_todos_opcionais_pode_ser_vazio(self):
        """DTO vazio deve ser válido (todos campos opcionais)."""
        dto = ProdutoUpdateDTO()

        assert dto.nome is None
        assert dto.preco is None
        assert dto.estoque is None

    def test_preco_invalido_falha(self):
        """Preço inválido deve falhar mesmo em update."""
        with pytest.raises(ValidationError):
            ProdutoUpdateDTO(preco=Decimal("0"))

    def test_estoque_negativo_falha(self):
        """Estoque negativo deve falhar."""
        with pytest.raises(ValidationError):
            ProdutoUpdateDTO(estoque=-1)

    def test_aplicar_na_entity_atualiza_apenas_campos_nao_none(self):
        """aplicar_na_entity deve atualizar apenas campos não-None."""
        from app.domain.entities.produto import Produto

        entity = Produto(id=1, nome="Original", preco=Decimal("100.00"), estoque=10)
        dto = ProdutoUpdateDTO(nome="Atualizado")

        dto.aplicar_na_entity(entity)

        assert entity.nome == "Atualizado"
        assert entity.preco == Decimal("100.00")  # Não mudou
        assert entity.estoque == 10  # Não mudou

    def test_preco_zero_falha_na_criacao_do_dto(self):
        """Preço zero deve falhar na criação do DTO."""
        with pytest.raises(ValidationError) as exc_info:
            ProdutoUpdateDTO(preco=Decimal("0"))

        errors = exc_info.value.errors()
        assert any(e["loc"][0] == "preco" for e in errors)


class TestProdutoResponseDTO:
    """Testes do DTO de resposta de produto."""

    def test_criar_com_todos_campos(self):
        """Deve criar DTO de resposta com todos os campos."""
        dto = ProdutoResponseDTO(
            id=1,
            nome="Teclado",
            preco=Decimal("150.00"),
            estoque=10,
        )

        assert dto.id == 1
        assert dto.nome == "Teclado"
        assert dto.preco == Decimal("150.00")
        assert dto.estoque == 10

    def test_from_entity_converte_corretamente(self):
        """from_entity deve converter entidade para DTO."""
        from app.domain.entities.produto import Produto

        entity = Produto(id=1, nome="Mouse", preco=Decimal("80.00"), estoque=5)
        dto = ProdutoResponseDTO.from_entity(entity)

        assert dto.id == 1
        assert dto.nome == "Mouse"
        assert dto.preco == Decimal("80.00")
        assert dto.estoque == 5

    def test_from_entity_requer_id(self):
        """from_entity deve falhar se entidade não tem ID."""
        from app.domain.entities.produto import Produto

        entity = Produto(nome="Mouse", preco=Decimal("80.00"), estoque=5)

        with pytest.raises(ValidationError) as exc_info:
            ProdutoResponseDTO.from_entity(entity)

        errors = exc_info.value.errors()
        assert any(e["loc"][0] == "id" for e in errors)

    def test_model_config_from_attributes(self):
        """Deve suportar from_attributes para ORM models."""
        from app.infrastructure.models.produto_model import ProdutoModel

        model = ProdutoModel(id=1, nome="Model", preco=Decimal("50.00"), estoque=3)
        dto = ProdutoResponseDTO.model_validate(model)

        assert dto.id == 1
        assert dto.nome == "Model"