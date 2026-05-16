import os

from dotenv import load_dotenv

load_dotenv()


def normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return "postgresql://" + url.removeprefix("postgres://")
    return url


def get_database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError("DATABASE_URL must be set")

    return normalize_database_url(url)


def get_base_url() -> str:
    return os.getenv("BASE_URL", "https://short.io").rstrip("/")
