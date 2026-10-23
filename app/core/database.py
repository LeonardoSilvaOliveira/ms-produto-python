"""
Configuração do banco de dados - SQLAlchemy Engine e Base.

Centraliza a criação do engine, session factory e metadata.
"""
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()


class Base(DeclarativeBase):
    """Base class para todos os models SQLAlchemy."""
    pass


# Configuração do engine
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    # Habilitar foreign keys no SQLite
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,  # Verifica conexão antes de usar
    echo=settings.DEBUG,  # Log SQL em modo debug
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    class_=Session,
)


def create_tables() -> None:
    """
    Cria todas as tabelas definidas nos models.

    Nota: Em produção, usar Alembic para migrações.
    Esta função é útil para desenvolvimento e testes.
    """
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    """Remove todas as tabelas (útil para testes)."""
    Base.metadata.drop_all(bind=engine)


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager para obter sessão do banco.

    Uso:
        with get_db_session() as db:
            produto = db.query(Produto).first()

    Garante fechamento automático da sessão.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para FastAPI - fornece sessão do banco por request.

    Uso em routes:
        @router.get("/produtos")
        def listar(db: Session = Depends(get_db)):
            ...

    O FastAPI gerencia o ciclo de vida (abre no início, fecha no fim).
    Commit automático em sucesso, rollback em erro.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        if settings.DEBUG:
            print(f"[DB] Rolling back session due to exception")
        db.rollback()
        raise
    else:
        if settings.DEBUG:
            print(f"[DB] Committing session")
        db.commit()
    finally:
        if settings.DEBUG:
            print(f"[DB] Closing session")
        db.close()