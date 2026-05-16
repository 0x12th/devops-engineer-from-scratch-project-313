import os
from typing import Any

from app.models import Link


def link_to_dict(link: Link) -> dict[str, Any]:
    base_url = (os.getenv("BASE_URL") or "https://short.io").rstrip("/")
    return {
        "id": link.id,
        "original_url": link.original_url,
        "short_name": link.short_name,
        "short_url": f"{base_url}/r/{link.short_name}",
    }
