"""
Configuração centralizada da aplicação usando Pydantic Settings.

Equivalente ao application.yml do Spring Boot.
Carrega variáveis de ambiente automaticamente do arquivo .env
"""
from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação carregadas via variáveis de ambiente."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Ambiente
    ENVIRONMENT: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Ambiente de execução",
    )
    DEBUG: bool = Field(default=True, description="Modo debug ativo")

    # Aplicação
    APP_NAME: str = Field(default="MS Produtos", description="Nome da aplicação")
    APP_VERSION: str = Field(default="1.0.0", description="Versão da aplicação")
    API_PREFIX: str = Field(default="/api/v1", description="Prefixo das rotas da API")

    # Banco de Dados
    DATABASE_URL: str = Field(
        default="sqlite:///./produtos.db",
        description="URL de conexão com o banco de dados",
    )
    # Para Oracle: oracle+oracledb://USUARIO:SENHA@host:porta/?service_name=XEPDB1

    # Segurança (para implementação futura de JWT)
    SECRET_KEY: str = Field(
        default="dev-secret-key-change-in-production",
        description="Chave secreta para assinatura de tokens JWT",
    )
    ALGORITHM: str = Field(default="HS256", description="Algoritmo de hash JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, description="Tempo de expiração do token de acesso (minutos)"
    )

    # CORS
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Origens permitidas para CORS",
    )

    # Logs
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO", description="Nível de log"
    )
    LOG_FORMAT: Literal["json", "text"] = Field(
        default="text", description="Formato do log"
    )


@lru_cache
def get_settings() -> Settings:
    """
    Retorna instância singleton das configurações.

    O @lru_cache garante que as configurações sejam carregadas apenas uma vez
    e reutilizadas em toda a aplicação (padrão singleton).
    """
    return Settings()


# Instância global para uso direto (opcional, preferir injeção via Depends)
settings = get_settings()