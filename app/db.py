from collections.abc import Generator

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

from app.config import get_database_url

engine = create_engine(get_database_url(), echo=False, pool_pre_ping=True)


def get_engine() -> Engine:
    return engine


def init_db(db_engine: Engine = engine) -> None:
    SQLModel.metadata.create_all(db_engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
