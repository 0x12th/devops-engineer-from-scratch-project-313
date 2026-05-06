from typing import Any

from app.config import get_base_url
from app.models import Link


def link_to_dict(link: Link) -> dict[str, Any]:
    return {
        "id": link.id,
        "original_url": link.original_url,
        "short_name": link.short_name,
        "short_url": f"{get_base_url()}/r/{link.short_name}",
    }
