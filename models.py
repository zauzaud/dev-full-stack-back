"""
Modelos do banco de dados para o sistema de Colecao de Games.

Este modulo define as tabelas do banco SQLite usando SQLAlchemy:
- Platform: Plataformas de jogos (PC, PS5, Xbox, etc.)
- Genre: Generos de jogos (RPG, FPS, Aventura, etc.)
- Game: Jogos cadastrados pelo usuario
- game_platforms: Tabela de associacao N:N entre Game e Platform
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Tabela de associacao N:N entre Game e Platform
game_platforms = Table(
    'game_platforms',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id'), primary_key=True),
    Column('platform_id', Integer, ForeignKey('platforms.id'), primary_key=True)
)


class Platform(Base):
    """Modelo para plataformas de jogos."""
    __tablename__ = 'platforms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    manufacturer = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    # Relacionamento com games
    games = relationship('Game', secondary=game_platforms, back_populates='platforms')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'manufacturer': self.manufacturer,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Genre(Base):
    """Modelo para generos de jogos."""
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    # Relacionamento com games
    games = relationship('Game', back_populates='genre')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Game(Base):
    """Modelo para jogos cadastrados."""
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    release_date = Column(Date, nullable=True)
    rating = Column(Float, nullable=True)  # Nota de 0 a 10
    hours_played = Column(Float, default=0)  # Horas jogadas
    status = Column(String(50), default='backlog')  # backlog, playing, completed, abandoned
    cover_url = Column(String(500), nullable=True)  # URL da capa do jogo
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relacionamentos
    genre = relationship('Genre', back_populates='games')
    platforms = relationship('Platform', secondary=game_platforms, back_populates='games')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'rating': self.rating,
            'hours_played': self.hours_played,
            'status': self.status,
            'cover_url': self.cover_url,
            'genre': self.genre.to_dict() if self.genre else None,
            'platforms': [p.to_dict() for p in self.platforms],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
