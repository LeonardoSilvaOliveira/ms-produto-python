"""
Core module - Configuração central, segurança e database.
"""
from app.core.config import Settings, get_settings, settings
from app.core.database import Base, create_tables, drop_tables, engine, get_db, get_db_session, SessionLocal
from app.core.security import (
    create_access_token,
    decode_token,
    get_password_hash,
    verify_password,
)

__all__ = [
    # Config
    "Settings",
    "get_settings",
    "settings",
    # Database
    "Base",
    "create_tables",
    "drop_tables",
    "engine",
    "get_db",
    "get_db_session",
    "SessionLocal",
    # Security
    "create_access_token",
    "decode_token",
    "get_password_hash",
    "verify_password",
]