"""
API REST para gerenciamento de Colecao de Games.

Uma API para catalogar jogos que voce ja jogou, com avaliacoes,
status de progresso, plataformas e generos.
"""

from datetime import datetime
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag

from database import init_db, get_db
from models import Game, Platform, Genre
from schemas import (
    GameCreate, GameUpdate, GameResponse, GameQuery, GameListResponse, GamePath,
    PlatformCreate, PlatformResponse, PlatformListResponse,
    GenreCreate, GenreResponse, GenreListResponse,
    MessageResponse, ErrorResponse
)

# Configuracao da API
info = Info(
    title="Colecao de Games API",
    version="1.0.0",
    description="API para gerenciar sua colecao pessoal de jogos. "
                "Cadastre jogos que voce jogou, de notas, registre horas jogadas "
                "e acompanhe seu progresso!"
)

app = OpenAPI(__name__, info=info)
CORS(app)

# Tags para organizacao no Swagger
game_tag = Tag(name="Games", description="Operacoes relacionadas a jogos")
platform_tag = Tag(name="Platforms", description="Operacoes relacionadas a plataformas")
genre_tag = Tag(name="Genres", description="Operacoes relacionadas a generos")

# Inicializa o banco de dados
init_db()


# ==================== ROTAS DE GAMES ====================

@app.post('/games', tags=[game_tag],
          responses={"201": GameResponse, "400": ErrorResponse})
def create_game(body: GameCreate):
    """
    Cadastra um novo jogo na colecao.

    Adiciona um jogo com titulo, descricao, nota, horas jogadas, status,
    genero e plataformas.
    """
    db = get_db()
    try:
        # Converte data se fornecida
        release_date = None
        if body.release_date:
            try:
                release_date = datetime.strptime(body.release_date, "%Y-%m-%d").date()
            except ValueError:
                return {"error": "Formato de data invalido. Use YYYY-MM-DD"}, 400

        # Cria o jogo
        game = Game(
            title=body.title,
            description=body.description,
            release_date=release_date,
            rating=body.rating,
            hours_played=body.hours_played or 0,
            status=body.status or "backlog",
            cover_url=body.cover_url,
            genre_id=body.genre_id
        )

        # Adiciona plataformas se fornecidas
        if body.platform_ids:
            platforms = db.query(Platform).filter(Platform.id.in_(body.platform_ids)).all()
            game.platforms = platforms

        db.add(game)
        db.commit()
        db.refresh(game)

        return game.to_dict(), 201
    except Exception as e:
        db.rollback()
        return {"error": str(e)}, 400
    finally:
        db.close()


@app.get('/games', tags=[game_tag],
         responses={"200": GameListResponse})
def get_games(query: GameQuery):
    """
    Lista todos os jogos da colecao.

    Retorna todos os jogos cadastrados. Pode filtrar por status ou genero.
    """
    db = get_db()
    try:
        games_query = db.query(Game)

        # Aplica filtros opcionais
        if query.status:
            games_query = games_query.filter(Game.status == query.status)
        if query.genre_id:
            games_query = games_query.filter(Game.genre_id == query.genre_id)

        games = games_query.order_by(Game.created_at.desc()).all()
        return {"games": [game.to_dict() for game in games]}, 200
    finally:
        db.close()


@app.get('/games/<int:game_id>', tags=[game_tag],
         responses={"200": GameResponse, "404": ErrorResponse})
def get_game(path: GamePath):
    """
    Busca um jogo pelo ID.

    Retorna os detalhes completos de um jogo especifico.
    """
    db = get_db()
    try:
        game = db.query(Game).filter(Game.id == path.game_id).first()
        if not game:
            return {"error": "Jogo nao encontrado"}, 404
        return game.to_dict(), 200
    finally:
        db.close()


@app.patch('/games/<int:game_id>', tags=[game_tag],
           responses={"200": GameResponse, "404": ErrorResponse})
def update_game(path: GamePath, body: GameUpdate):
    """
    Atualiza parcialmente um jogo existente (PATCH).

    Diferente do PUT que substitui o recurso inteiro, o PATCH permite
    atualizar apenas os campos enviados na requisicao. Campos nao
    enviados permanecem inalterados.

    Exemplo: enviar apenas {"rating": 9.0} atualiza somente a nota,
    mantendo todos os outros campos do jogo.
    """
    db = get_db()
    try:
        game = db.query(Game).filter(Game.id == path.game_id).first()
        if not game:
            return {"error": "Jogo nao encontrado"}, 404

        # Atualiza campos fornecidos
        if body.title is not None:
            game.title = body.title
        if body.description is not None:
            game.description = body.description
        if body.release_date is not None:
            try:
                game.release_date = datetime.strptime(body.release_date, "%Y-%m-%d").date()
            except ValueError:
                return {"error": "Formato de data invalido. Use YYYY-MM-DD"}, 400
        if body.rating is not None:
            game.rating = body.rating
        if body.hours_played is not None:
            game.hours_played = body.hours_played
        if body.status is not None:
            game.status = body.status
        if body.cover_url is not None:
            game.cover_url = body.cover_url
        if body.genre_id is not None:
            game.genre_id = body.genre_id
        if body.platform_ids is not None:
            platforms = db.query(Platform).filter(Platform.id.in_(body.platform_ids)).all()
            game.platforms = platforms

        db.commit()
        db.refresh(game)

        return game.to_dict(), 200
    except Exception as e:
        db.rollback()
        return {"error": str(e)}, 400
    finally:
        db.close()


@app.delete('/games/<int:game_id>', tags=[game_tag],
            responses={"200": MessageResponse, "404": ErrorResponse})
def delete_game(path: GamePath):
    """
    Remove um jogo da colecao.

    Deleta permanentemente o jogo especificado.
    """
    db = get_db()
    try:
        game = db.query(Game).filter(Game.id == path.game_id).first()
        if not game:
            return {"error": "Jogo nao encontrado"}, 404

        title = game.title
        db.delete(game)
        db.commit()

        return {"message": f"Jogo '{title}' removido com sucesso"}, 200
    finally:
        db.close()


# ==================== ROTAS DE PLATFORMS ====================

@app.get('/platforms', tags=[platform_tag],
         responses={"200": PlatformListResponse})
def get_platforms():
    """
    Lista todas as plataformas.

    Retorna todas as plataformas de jogos cadastradas (PC, PS5, Xbox, etc).
    """
    db = get_db()
    try:
        platforms = db.query(Platform).order_by(Platform.name).all()
        return {"platforms": [p.to_dict() for p in platforms]}, 200
    finally:
        db.close()


@app.post('/platforms', tags=[platform_tag],
          responses={"201": PlatformResponse, "400": ErrorResponse})
def create_platform(body: PlatformCreate):
    """
    Cadastra uma nova plataforma.

    Adiciona uma plataforma de jogos (ex: PlayStation 5, Xbox Series X, PC).
    """
    db = get_db()
    try:
        # Verifica se ja existe
        existing = db.query(Platform).filter(Platform.name == body.name).first()
        if existing:
            return {"error": "Plataforma ja cadastrada"}, 400

        platform = Platform(
            name=body.name,
            manufacturer=body.manufacturer
        )
        db.add(platform)
        db.commit()
        db.refresh(platform)

        return platform.to_dict(), 201
    except Exception as e:
        db.rollback()
        return {"error": str(e)}, 400
    finally:
        db.close()


# ==================== ROTAS DE GENRES ====================

@app.get('/genres', tags=[genre_tag],
         responses={"200": GenreListResponse})
def get_genres():
    """
    Lista todos os generos.

    Retorna todos os generos de jogos cadastrados (RPG, FPS, Aventura, etc).
    """
    db = get_db()
    try:
        genres = db.query(Genre).order_by(Genre.name).all()
        return {"genres": [g.to_dict() for g in genres]}, 200
    finally:
        db.close()


@app.post('/genres', tags=[genre_tag],
          responses={"201": GenreResponse, "400": ErrorResponse})
def create_genre(body: GenreCreate):
    """
    Cadastra um novo genero.

    Adiciona um genero de jogo (ex: RPG, FPS, Aventura, Puzzle).
    """
    db = get_db()
    try:
        # Verifica se ja existe
        existing = db.query(Genre).filter(Genre.name == body.name).first()
        if existing:
            return {"error": "Genero ja cadastrado"}, 400

        genre = Genre(
            name=body.name,
            description=body.description
        )
        db.add(genre)
        db.commit()
        db.refresh(genre)

        return genre.to_dict(), 201
    except Exception as e:
        db.rollback()
        return {"error": str(e)}, 400
    finally:
        db.close()


# ==================== INICIALIZACAO ====================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
