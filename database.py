"""
Configuracao do banco de dados SQLite.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Configuracao do SQLite
DATABASE_URL = "sqlite:///./database/games_collection.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Inicializa o banco de dados criando todas as tabelas."""
    import os
    os.makedirs('./database', exist_ok=True)
    Base.metadata.create_all(bind=engine)


def get_db():
    """Retorna uma sessao do banco de dados."""
    db = SessionLocal()
    try:
        return db
    finally:
        pass
