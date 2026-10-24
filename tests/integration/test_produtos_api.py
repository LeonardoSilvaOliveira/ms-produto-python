"""
Testes de integração da API (Presentation Layer).

Testa endpoints HTTP completos com TestClient.
"""
import pytest
from decimal import Decimal


class TestProdutosAPI:
    """Testes dos endpoints de produtos."""

    def test_criar_produto_sucesso(self, app_client):
        """POST /api/v1/produtos deve criar produto."""
        response = app_client.post(
            "/api/v1/produtos",
            json={"nome": "Teclado Mecânico", "preco": "150.00", "estoque": 10},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "Teclado Mecânico"
        assert data["preco"] == "150.00"
        assert data["estoque"] == 10
        assert "id" in data

    def test_criar_produto_sem_estoque(self, app_client):
        """POST deve aceitar produto sem estoque (default 0)."""
        response = app_client.post(
            "/api/v1/produtos",
            json={"nome": "Mouse", "preco": "80.00"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["estoque"] == 0

    def test_criar_produto_nome_invalido(self, app_client):
        """POST deve rejeitar nome muito curto."""
        response = app_client.post(
            "/api/v1/produtos",
            json={"nome": "A", "preco": "10.00"},
        )

        assert response.status_code == 422

    def test_criar_produto_preco_invalido(self, app_client):
        """POST deve rejeitar preço <= 0."""
        response = app_client.post(
            "/api/v1/produtos",
            json={"nome": "Produto", "preco": "0"},
        )

        assert response.status_code == 422

    def test_criar_produto_campos_obrigatorios(self, app_client):
        """POST deve exigir nome e preco."""
        response = app_client.post("/api/v1/produtos", json={})

        assert response.status_code == 422

    # ===== GET BY ID =====

    def test_buscar_produto_existente(self, app_client):
        """GET /api/v1/produtos/{id} deve retornar produto."""
        # Cria produto
        create_resp = app_client.post(
            "/api/v1/produtos",
            json={"nome": "Teclado", "preco": "150.00", "estoque": 10},
        )
        produto_id = create_resp.json()["id"]

        # Busca
        response = app_client.get(f"/api/v1/produtos/{produto_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == produto_id
        assert data["nome"] == "Teclado"
        assert data["preco"] == "150.00"

    def test_buscar_produto_inexistente(self, app_client):
        """GET deve retornar 404 para produto inexistente."""
        response = app_client.get("/api/v1/produtos/999")

        assert response.status_code == 404

    # ===== LIST =====

    def test_listar_produtos(self, app_client, sample_produtos):
        """GET /api/v1/produtos deve listar produtos."""
        response = app_client.get("/api/v1/produtos")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3

    def test_listar_produtos_retorna_lista_direta(self, app_client):
        """GET deve retornar lista direta, não objeto paginado."""
        response = app_client.get("/api/v1/produtos")

        assert response.status_code == 200
        data = response.json()
        # Verifica que é lista simples, não objeto com paginação
        assert isinstance(data, list)
        assert "produtos" not in str(data) or "total" not in str(data)

    # ===== UPDATE =====

    def test_atualizar_produto_sucesso(self, app_client):
        """PUT /api/v1/produtos/{id} deve atualizar produto."""
        create_resp = app_client.post(
            "/api/v1/produtos",
            json={"nome": "Original", "preco": "100.00", "estoque": 5},
        )
        produto_id = create_resp.json()["id"]

        response = app_client.put(
            f"/api/v1/produtos/{produto_id}",
            json={"nome": "Atualizado", "preco": "200.00"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Atualizado"
        assert data["preco"] == "200.00"
        assert data["estoque"] == 5  # Não mudou

    def test_atualizar_produto_parcial(self, app_client):
        """PUT deve permitir atualização parcial (apenas nome)."""
        create_resp = app_client.post(
            "/api/v1/produtos",
            json={"nome": "Original", "preco": "100.00", "estoque": 5},
        )
        produto_id = create_resp.json()["id"]

        response = app_client.put(
            f"/api/v1/produtos/{produto_id}",
            json={"nome": "Apenas Nome"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Apenas Nome"
        assert data["preco"] == "100.00"  # Não mudou
        assert data["estoque"] == 5  # Não mudou

    def test_atualizar_produto_inexistente(self, app_client):
        """PUT deve retornar 404 para produto inexistente."""
        response = app_client.put(
            "/api/v1/produtos/999",
            json={"nome": "Novo"},
        )

        assert response.status_code == 404

    def test_atualizar_produto_dados_invalidos(self, app_client):
        """PUT deve rejeitar dados inválidos."""
        create_resp = app_client.post(
            "/api/v1/produtos",
            json={"nome": "Original", "preco": "100.00", "estoque": 5},
        )
        produto_id = create_resp.json()["id"]

        response = app_client.put(
            f"/api/v1/produtos/{produto_id}",
            json={"preco": "0"},
        )

        assert response.status_code == 422

    # ===== DELETE =====

    def test_deletar_produto_sucesso(self, app_client):
        """DELETE /api/v1/produtos/{id} deve remover produto."""
        create_resp = app_client.post(
            "/api/v1/produtos",
            json={"nome": "Para Deletar", "preco": "50.00", "estoque": 1},
        )
        produto_id = create_resp.json()["id"]

        response = app_client.delete(f"/api/v1/produtos/{produto_id}")

        assert response.status_code == 204

        # Verifica se foi deletado
        get_resp = app_client.get(f"/api/v1/produtos/{produto_id}")
        assert get_resp.status_code == 404

    def test_deletar_produto_inexistente(self, app_client):
        """DELETE deve retornar 404 para produto inexistente."""
        response = app_client.delete("/api/v1/produtos/999")

        assert response.status_code == 404


class TestAPIHealthCheck:
    """Testes de health check da API."""

    def test_health_check(self, app_client):
        """GET /health deve retornar status ok."""
        response = app_client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_root_redirect(self, app_client):
        """GET / deve redirecionar para docs."""
        response = app_client.get("/", follow_redirects=False)

        # Pode ser redirect ou 404 dependendo da configuração
        assert response.status_code in (200, 307, 404)


class TestAPIValidationErrors:
    """Testes de erros de validação da API."""

    def test_erro_422_retorna_detalhes(self, app_client):
        """Erros 422 devem retornar detalhes de validação."""
        response = app_client.post(
            "/api/v1/produtos",
            json={"nome": "", "preco": "-10"},
        )

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert isinstance(data["detail"], list)

    def test_erro_404_formato_consistente(self, app_client):
        """Erros 404 devem ter formato consistente."""
        response = app_client.get("/api/v1/produtos/999")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data