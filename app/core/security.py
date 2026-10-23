"""
Módulo de segurança - Esqueleto para implementação futura de JWT.

Quando implementar autenticação, adicione aqui:
- Criação e validação de tokens JWT
- Hash de senhas com bcrypt
- Dependências para usuário atual
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

# Context para hash de senhas (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token de acesso JWT.

    Args:
        data: Dados a serem codificados no token (ex: {"sub": user_email})
        expires_delta: Tempo de expiração customizado

    Returns:
        Token JWT assinado
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto plano corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Gera hash bcrypt da senha."""
    return pwd_context.hash(password)


def decode_token(token: str) -> Optional[dict]:
    """
    Decodifica e valida um token JWT.

    Returns:
        Payload do token se válido, None se inválido/expirado
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.JWTError:
        return None