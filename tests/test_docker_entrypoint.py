from pathlib import Path


def test_nginx_config_uses_backend_port_template():
    nginx_config = Path(".configs/nginx.conf").read_text()
    entrypoint = Path(".scripts/docker-entrypoint.sh").read_text()

    assert "127.0.0.1:8080" not in nginx_config
    assert "127.0.0.1:__BACKEND_PORT__" in nginx_config
    assert "listen __PORT__;" in nginx_config
    assert "nginx.conf.template" in entrypoint
    assert "s/__BACKEND_PORT__/${BACKEND_PORT}/g" in entrypoint
    assert "s/__PORT__/${PORT}/g" in entrypoint
    assert "uv run gunicorn" not in entrypoint
    assert "/app/.venv/bin/gunicorn" in entrypoint
    assert "app.main:app" in entrypoint
