"""
Schemas Pydantic para validacao e documentacao da API.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


# ==================== PLATFORM ====================

class PlatformCreate(BaseModel):
    """Schema para criacao de plataforma."""
    name: str = Field(..., description="Nome da plataforma")
    manufacturer: Optional[str] = Field(None, description="Fabricante")


class PlatformResponse(BaseModel):
    """Schema de resposta para plataforma."""
    id: int
    name: str
    manufacturer: Optional[str]
    created_at: Optional[str]


# ==================== GENRE ====================

class GenreCreate(BaseModel):
    """Schema para criacao de genero."""
    name: str = Field(..., description="Nome do genero")
    description: Optional[str] = Field(None, description="Descricao do genero")


class GenreResponse(BaseModel):
    """Schema de resposta para genero."""
    id: int
    name: str
    description: Optional[str]
    created_at: Optional[str]


# ==================== GAME ====================

class GameCreate(BaseModel):
    """Schema para criacao de jogo."""
    title: str = Field(..., description="Titulo do jogo")
    description: Optional[str] = Field(None, description="Descricao do jogo")
    release_date: Optional[str] = Field(None, description="Data de lancamento (YYYY-MM-DD)")
    rating: Optional[float] = Field(None, ge=0, le=10, description="Nota de 0 a 10")
    hours_played: Optional[float] = Field(0, ge=0, description="Horas jogadas")
    status: Optional[str] = Field("backlog", description="Status: backlog, playing, completed, abandoned")
    cover_url: Optional[str] = Field(None, description="URL da imagem de capa")
    genre_id: Optional[int] = Field(None, description="ID do genero")
    platform_ids: Optional[List[int]] = Field([], description="Lista de IDs das plataformas")


class GameUpdate(BaseModel):
    """Schema para atualizacao de jogo."""
    title: Optional[str] = Field(None, description="Titulo do jogo")
    description: Optional[str] = Field(None, description="Descricao do jogo")
    release_date: Optional[str] = Field(None, description="Data de lancamento (YYYY-MM-DD)")
    rating: Optional[float] = Field(None, ge=0, le=10, description="Nota de 0 a 10")
    hours_played: Optional[float] = Field(None, ge=0, description="Horas jogadas")
    status: Optional[str] = Field(None, description="Status: backlog, playing, completed, abandoned")
    cover_url: Optional[str] = Field(None, description="URL da imagem de capa")
    genre_id: Optional[int] = Field(None, description="ID do genero")
    platform_ids: Optional[List[int]] = Field(None, description="Lista de IDs das plataformas")


class GameResponse(BaseModel):
    """Schema de resposta para jogo."""
    id: int
    title: str
    description: Optional[str]
    release_date: Optional[str]
    rating: Optional[float]
    hours_played: Optional[float]
    status: Optional[str]
    cover_url: Optional[str]
    genre: Optional[GenreResponse]
    platforms: List[PlatformResponse]
    created_at: Optional[str]
    updated_at: Optional[str]


# ==================== RESPOSTAS DE LISTA ====================

class GameListResponse(BaseModel):
    """Schema de resposta para lista de jogos."""
    games: List[GameResponse]


class PlatformListResponse(BaseModel):
    """Schema de resposta para lista de plataformas."""
    platforms: List[PlatformResponse]


class GenreListResponse(BaseModel):
    """Schema de resposta para lista de generos."""
    genres: List[GenreResponse]


# ==================== RESPOSTAS GERAIS ====================

class MessageResponse(BaseModel):
    """Schema para mensagens de resposta."""
    message: str = Field(..., description="Mensagem de resposta")


class ErrorResponse(BaseModel):
    """Schema para respostas de erro."""
    error: str = Field(..., description="Mensagem de erro")


# ==================== QUERY PARAMETERS ====================

class GameQuery(BaseModel):
    """Query parameters para busca de jogos."""
    status: Optional[str] = Field(None, description="Filtrar por status")
    genre_id: Optional[int] = Field(None, description="Filtrar por genero")


# ==================== PATH PARAMETERS ====================

class GamePath(BaseModel):
    """Path parameter para identificar um jogo."""
    game_id: int = Field(..., description="ID do jogo")
