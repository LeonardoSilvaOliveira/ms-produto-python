"""
Configuração compartilhada de testes (pytest fixtures).

Fixtures disponíveis:
- app_client: TestClient do FastAPI para testes de API
- db_session: Session SQLAlchemy isolada por teste (com rollback automático)
- override_get_db: Dependency override para injetar session de teste
- produto_factory: Factory para criar produtos de teste (usando Faker)
"""
import os
import sys
from decimal import Decimal
from typing import Generator

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

# Adicionar raiz do projeto ao path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import get_settings
from app.core.database import Base, get_db
from app.infrastructure.models.produto_model import ProdutoModel
from app.main import create_app

# Configuração
settings = get_settings()
fake = Faker("pt_BR")

# Engine de teste (SQLite em memória para velocidade)
TEST_DATABASE_URL = "sqlite:///:memory:"

# Para PostgreSQL no CI, usar variável de ambiente
if os.getenv("DATABASE_URL"):
    TEST_DATABASE_URL = os.getenv("DATABASE_URL")

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False} if TEST_DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=True,
)

# Habilitar foreign keys no SQLite
if TEST_DATABASE_URL.startswith("sqlite"):
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
    class_=Session,
)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """Cria tabelas uma vez por sessão de testes."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Session de banco isolada por teste.

    Cada teste roda em uma transação que é feita rollback no final,
    garantindo isolamento total entre testes.
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def app_client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    TestClient do FastAPI com dependency override para db_session.

    Uso:
        def test_algo(app_client):
            response = app_client.get("/api/v1/produtos")
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # db_session é gerenciado pelo fixture db_session

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def produto_factory(db_session: Session):
    """
    Factory para criar produtos de teste no banco.

    Uso:
        def test_algo(produto_factory):
            produto = produto_factory(nome="Meu Produto", preco=Decimal("100.00"))
    """
    def _create(
        nome: str = None,
        preco: Decimal = None,
        estoque: int = None,
    ) -> ProdutoModel:
        produto = ProdutoModel(
            nome=nome or fake.unique.word().capitalize() + " " + fake.word().capitalize(),
            preco=preco or Decimal(str(fake.pydecimal(left_digits=3, right_digits=2, positive=True))),
            estoque=estoque if estoque is not None else fake.random_int(min=0, max=100),
        )
        db_session.add(produto)
        db_session.flush()
        db_session.refresh(produto)
        return produto

    return _create


@pytest.fixture
def produto_data():
    """Dados válidos para criação de produto (para testes de API)."""
    return {
        "nome": fake.unique.word().capitalize() + " " + fake.word().capitalize(),
        "preco": str(fake.pydecimal(left_digits=3, right_digits=2, positive=True)),
        "estoque": fake.random_int(min=0, max=100),
    }


# Fixtures de dados pré-definidos para testes consistentes
@pytest.fixture
def sample_produtos(db_session: Session) -> list[ProdutoModel]:
    """Cria lista de produtos de exemplo para testes de listagem."""
    produtos = [
        ProdutoModel(nome="Teclado Mecânico", preco=Decimal("150.00"), estoque=10),
        ProdutoModel(nome="Mouse Gamer", preco=Decimal("120.00"), estoque=15),
        ProdutoModel(nome="Monitor 27\"", preco=Decimal("899.90"), estoque=5),
    ]
    db_session.add_all(produtos)
    db_session.flush()
    for p in produtos:
        db_session.refresh(p)
    return produtos