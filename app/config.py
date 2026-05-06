import os

from dotenv import load_dotenv

load_dotenv()


def normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


def get_database_url() -> str:
    return normalize_database_url(os.getenv("DATABASE_URL", "sqlite:///./app.db"))


def get_base_url() -> str:
    return os.getenv("BASE_URL", "http://localhost:8080").rstrip("/")
