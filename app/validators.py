import json


def parse_range_header(value: str | None) -> tuple[int, int]:
    if not value:
        return 0, 9

    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError("range must be a JSON array") from exc

    if (
        not isinstance(parsed, list)
        or len(parsed) != 2
        or not all(isinstance(item, int) for item in parsed)
    ):
        raise ValueError("range must contain two integers")

    start, end = parsed
    if start < 0 or end < start:
        raise ValueError("range bounds are invalid")

    return start, end


def validate_short_name(short_name: str) -> str | None:
    if "/" in short_name:
        return "short_name must not contain path separators"
    return None
