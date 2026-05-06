from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, create_engine

from app.config import get_database_url


def create_db_engine() -> Engine:
    database_url = get_database_url()
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    return create_engine(database_url, connect_args=connect_args)


def init_db(engine: Engine) -> None:
    SQLModel.metadata.create_all(engine)
