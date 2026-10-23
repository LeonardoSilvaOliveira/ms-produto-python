# MS Produtos - Microsserviço em Python

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red?logo=sqlalchemy)](https://sqlalchemy.org)
[![Alembic](https://img.shields.io/badge/Alembic-1.13+-orange)](https://alembic.sqlalchemy.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

Microsserviço de gerenciamento de produtos construído com **FastAPI**, **SQLAlchemy 2.x** e **Clean Architecture**. Desenvolvido para portfolio e aprendizado avançado de Python.

---

## 🎯 Objetivos do Projeto

- ✅ Demonstrar conhecimento de **arquitetura limpa** em Python
- ✅ Aplicar **padrões de microserviços** (similar a Spring Boot/Java)
- ✅ Usar **tipagem estática** moderna (Pydantic v2, Python 3.10+)
- ✅ Configuração **12-factor app** com variáveis de ambiente
- ✅ **Migrações de banco** versionadas com Alembic
- ✅ Código **testável**, **extensível** e **documentado**

---

## 🚀 Stack Tecnológica

| Camada | Tecnologia |
|--------|------------|
| **API Framework** | FastAPI 0.115+ |
| **Validação/Config** | Pydantic v2 + pydantic-settings |
| **ORM** | SQLAlchemy 2.0 (async-ready) |
| **Migrations** | Alembic 1.13 |
| **Database (Dev)** | SQLite |
| **Database (Prod)** | Oracle (via oracledb) |
| **Security** | python-jose (JWT) + passlib (bcrypt) |
| **Testing** | pytest + httpx |
| **Server** | Uvicorn |

---

## 📁 Arquitetura (Clean Architecture)

```
app/
├── core/                    # Configuração central, segurança, database
│   ├── config.py           # Pydantic Settings (.env)
│   ├── security.py         # JWT, password hashing
│   └── database.py         # Engine, Session, Base
├── domain/                  # Camada de domínio (regras puras)
│   ├── entities/           # Entidades + validações de negócio
│   ├── repositories/       # Protocols/Interfaces (Dependency Inversion)
│   └── exceptions/         # Exceções de domínio
├── application/             # Casos de uso (Use Cases)
│   ├── dto/                # Data Transfer Objects internos
│   └── services/           # Orquestração (ProductService)
├── infrastructure/          # Implementações concretas
│   ├── models/             # SQLAlchemy Models (tabelas)
│   ├── repositories/       # Repository implementations
│   └── database/           # Session management
├── presentation/            # Camada HTTP (API)
│   ├── api/v1/
│   │   ├── routes/         # Endpoints (Controllers)
│   │   └── schemas/        # Request/Response Schemas
│   ├── api/deps.py         # Dependency Injection (FastAPI DI)
│   └── middleware/         # Logging, error handling
├── main.py                  # Entry point + lifespan
└── alembic/                 # Migrações versionadas
```

### Princípios aplicados
- **Dependency Inversion**: Domain define protocols, Infrastructure implementa
- **Single Responsibility**: Cada camada tem responsabilidade única
- **Open/Closed**: Fácil adicionar features sem modificar código existente
- **Interface Segregation**: Protocols pequenos e específicos

---

## 📦 Como Rodar

### Pré-requisitos
- Python 3.10+
- (Opcional) Oracle Client para produção

### Instalação
```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/ms-produto.git
cd ms-produto

# 2. Crie e ative virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows PowerShell

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure variáveis de ambiente
cp .env.example .env
# Edite .env se necessário (DATABASE_URL, SECRET_KEY, etc.)

# 5. Rode migrações
alembic upgrade head

# 6. Inicie a aplicação
uvicorn app.main:app --reload
```

### URLs úteis
| Recurso | URL |
|---------|-----|
| **Swagger UI** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **Health Check** | http://localhost:8000/health |
| **OpenAPI JSON** | http://localhost:8000/openapi.json |

---

## 🧪 Testando a API

### Via Swagger (Recomendado)
Acesse http://localhost:8000/docs e use "Try it out"

### Via curl / PowerShell
```bash
# Criar produto
curl -X POST http://localhost:8000/api/v1/produtos \
  -H "Content-Type: application/json" \
  -d '{"nome": "Teclado Mecânico", "preco": "150.00", "estoque": 10}'

# Listar todos
curl http://localhost:8000/api/v1/produtos

# Buscar por ID
curl http://localhost:8000/api/v1/produtos/1

# Atualizar (parcial)
curl -X PUT http://localhost:8000/api/v1/produtos/1 \
  -H "Content-Type: application/json" \
  -d '{"preco": "180.00"}'

# Deletar
curl -X DELETE http://localhost:8000/api/v1/produtos/1
```

### Via Python (httpx)
```python
import httpx

# Criar
r = httpx.post("http://localhost:8000/api/v1/produtos", 
               json={"nome": "Mouse", "preco": "80.00", "estoque": 20})
print(r.json())

# Listar
r = httpx.get("http://localhost:8000/api/v1/produtos")
print(r.json())
```

---

## 🗄️ Banco de Dados

### Desenvolvimento (SQLite)
Padrão no `.env.example`:
```
DATABASE_URL=sqlite:///./produtos.db
```

### Produção (Oracle)
```bash
# No .env
DATABASE_URL=oracle+oracledb://usuario:senha@host:1521/?service_name=XEPDB1

# Se usar Oracle Thick mode (requer Oracle Client instalado)
DATABASE_URL=oracle+oracledb://usuario:senha@host:1521/?service_name=XEPDB1&thick_mode=true
```

### Migrações
```bash
# Criar nova migração (após mudar models)
alembic revision --autogenerate -m "descrição da mudança"

# Aplicar migrações
alembic upgrade head

# Ver histórico
alembic history

# Rollback (1 versão)
alembic downgrade -1
```

---

## 🔐 Segurança (Preparado)

O módulo `app/core/security.py` já contém:
- **JWT**: Criação/validação de tokens (`create_access_token`, `decode_token`)
- **Password Hashing**: bcrypt via `passlib` (`get_password_hash`, `verify_password`)

Para ativar autenticação:
1. Implemente endpoint `/auth/login` em `presentation/api/v1/routes/auth.py`
2. Adicione dependency `get_current_user` em `presentation/api/deps.py`
3. Proteja rotas com `Depends(get_current_user)`

---

## 🧪 Testes

```bash
# Rodar todos
pytest -v

# Com coverage
pytest --cov=app --cov-report=html

# Apenas testes de integração
pytest tests/integration -v
```

> **Nota**: Estrutura de testes preparada, implementação na Fase 4.

---

## 🐳 Docker

```dockerfile
# Dockerfile (exemplo)
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build
docker build -t ms-produto .

# Run (SQLite persistido)
docker run -p 8000:8000 -v $(pwd)/produtos.db:/app/produtos.db ms-produto

# Run (Oracle via env)
docker run -p 8000:8000 --env-file .env ms-produto
```

---

## 📋 Roadmap

- [x] **Fase 1**: Clean Architecture + Config + Alembic
- [ ] **Fase 2**: Autenticação JWT + Roles (ADMIN/USER)
- [ ] **Fase 3**: Categorias, Paginação, Filtros, Busca
- [ ] **Fase 4**: Testes (pytest), CI/CD (GitHub Actions), Observabilidade
- [ ] **Fase 5**: Frontend React + TypeScript + Vite + Tailwind

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie branch: `git checkout -b feature/nova-feature`
3. Commit: `git commit -m 'feat: descrição da feature'`
4. Push: `git push origin feature/nova-feature`
5. Abra Pull Request

---

## 📄 Licença

Distribuído sob licença MIT. Veja `LICENSE` para detalhes.

---

## 👨‍💻 Autor

**Leonardo Silva Oliveira**

- GitHub: [@LeonardoSilvaOliveira](https://github.com/LeonardoSilvaOliveira)
- LinkedIn: [linkedin.com/in/leonardosilvaoliveira](https://linkedin.com/in/leonardosilvaoliveira)

> Projeto desenvolvido para portfolio e aprendizado de Python, inspirado em arquiteturas Java/Spring Boot.