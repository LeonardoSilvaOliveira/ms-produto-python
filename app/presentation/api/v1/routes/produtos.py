"""
Routes da API v1 - Produtos.

Endpoints HTTP para gerenciamento de produtos.
Usa ProdutoService via injeção de dependência (não acessa DB diretamente).
"""
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services.produto_service import ProdutoService
from app.application.dto.produto_dto import ProdutoCreateDTO, ProdutoUpdateDTO
from app.domain.exceptions import (
    EntidadeNaoEncontrada,
    RegraDeNegocioViolada,
    DadosInvalidos,
)
from app.presentation.api.deps import get_produto_service
from app.presentation.api.v1.schemas.produto_schemas import (
    ProdutoCreateRequest,
    ProdutoUpdateRequest,
    ProdutoResponse,
    MessageResponse,
    ErrorResponse,
)

router = APIRouter(prefix="/produtos", tags=["Produtos"])


# Mapeamento de exceções de domínio para HTTP
def _handle_domain_exception(e: Exception) -> HTTPException:
    """Converte exceções de domínio em HTTPException."""
    if isinstance(e, EntidadeNaoEncontrada):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    if isinstance(e, RegraDeNegocioViolada):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    if isinstance(e, DadosInvalidos):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        )
    # Erro inesperado
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Erro interno do servidor",
    )


@router.post(
    "",
    response_model=ProdutoResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Dados inválidos ou regra de negócio violada"},
        422: {"model": ErrorResponse, "description": "Erro de validação"},
    },
    summary="Criar novo produto",
    description="Cria um novo produto no sistema.",
)
def criar_produto(
    request: ProdutoCreateRequest,
    service: ProdutoService = Depends(get_produto_service),
) -> ProdutoResponse:
    """
    Cria um novo produto.

    - **nome**: Nome do produto (2-100 caracteres)
    - **preco**: Preço maior que zero
    - **estoque**: Quantidade inicial (padrão 0)
    """
    try:
        dto = ProdutoCreateDTO(
            nome=request.nome,
            preco=request.preco,
            estoque=request.estoque,
        )
        result = service.criar_produto(dto)
        return ProdutoResponse.model_validate(result)
    except (RegraDeNegocioViolada, DadosInvalidos, EntidadeNaoEncontrada) as e:
        raise _handle_domain_exception(e)


@router.get(
    "",
    response_model=list[ProdutoResponse],
    summary="Listar todos os produtos",
    description="Retorna lista de todos os produtos cadastrados.",
)
def listar_produtos(
    service: ProdutoService = Depends(get_produto_service),
) -> list[ProdutoResponse]:
    """Lista todos os produtos."""
    try:
        produtos = service.listar_produtos()
        return [ProdutoResponse.model_validate(p) for p in produtos]
    except (RegraDeNegocioViolada, DadosInvalidos, EntidadeNaoEncontrada) as e:
        raise _handle_domain_exception(e)


@router.get(
    "/{produto_id}",
    response_model=ProdutoResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Produto não encontrado"},
    },
    summary="Buscar produto por ID",
    description="Retorna um produto específico pelo seu ID.",
)
def buscar_produto(
    produto_id: int,
    service: ProdutoService = Depends(get_produto_service),
) -> ProdutoResponse:
    """
    Busca um produto pelo ID.

    - **produto_id**: ID do produto
    """
    try:
        produto = service.buscar_produto(produto_id)
        return ProdutoResponse.model_validate(produto)
    except (RegraDeNegocioViolada, DadosInvalidos, EntidadeNaoEncontrada) as e:
        raise _handle_domain_exception(e)


@router.put(
    "/{produto_id}",
    response_model=ProdutoResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Dados inválidos ou regra de negócio violada"},
        404: {"model": ErrorResponse, "description": "Produto não encontrado"},
        422: {"model": ErrorResponse, "description": "Erro de validação"},
    },
    summary="Atualizar produto",
    description="Atualiza um produto existente. Apenas campos enviados são atualizados.",
)
def atualizar_produto(
    produto_id: int,
    request: ProdutoUpdateRequest,
    service: ProdutoService = Depends(get_produto_service),
) -> ProdutoResponse:
    """
    Atualiza um produto existente.

    - **produto_id**: ID do produto
    - **nome**: (opcional) Novo nome (2-100 caracteres)
    - **preco**: (opcional) Novo preço (> 0)
    - **estoque**: (opcional) Novo estoque (>= 0)
    """
    try:
        # Converte request para DTO (apenas campos não-None)
        dto = ProdutoUpdateDTO(
            nome=request.nome,
            preco=request.preco,
            estoque=request.estoque,
        )
        result = service.atualizar_produto(produto_id, dto)
        return ProdutoResponse.model_validate(result)
    except (RegraDeNegocioViolada, DadosInvalidos, EntidadeNaoEncontrada) as e:
        raise _handle_domain_exception(e)


@router.delete(
    "/{produto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Produto não encontrado"},
    },
    summary="Remover produto",
    description="Remove um produto do sistema.",
)
def remover_produto(
    produto_id: int,
    service: ProdutoService = Depends(get_produto_service),
) -> None:
    """
    Remove um produto pelo ID.

    - **produto_id**: ID do produto a remover
    """
    try:
        service.remover_produto(produto_id)
    except (RegraDeNegocioViolada, DadosInvalidos, EntidadeNaoEncontrada) as e:
        raise _handle_domain_exception(e)