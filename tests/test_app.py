import pytest


@pytest.fixture
def client(monkeypatch, tmp_path):
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    monkeypatch.setenv("DATABASE_URL", database_url)
    monkeypatch.setenv("BASE_URL", "http://localhost:8080")

    from app.main import create_app

    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def create_link(client, original_url="https://example.com/long-url", short_name="exmpl"):
    return client.post(
        "/api/links",
        json={"original_url": original_url, "short_name": short_name},
    )


def test_ping(client):
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.text == "pong"


def test_create_link(client):
    response = create_link(client)

    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "original_url": "https://example.com/long-url",
        "short_name": "exmpl",
        "short_url": "http://localhost:8080/r/exmpl",
    }


def test_create_link_validates_required_fields(client):
    response = client.post("/api/links", json={"original_url": "https://example.com"})

    assert response.status_code == 400
    assert response.get_json() == {"error": "original_url and short_name are required"}


def test_create_link_rejects_duplicate_short_name(client):
    create_link(client)
    response = create_link(client, original_url="https://example.com/another")

    assert response.status_code == 409
    assert response.get_json() == {"error": "short_name already exists"}


def test_create_link_rejects_short_name_with_path_separator(client):
    response = create_link(client, short_name="a/b")

    assert response.status_code == 400
    assert response.get_json() == {"error": "short_name must not contain path separators"}


def test_list_links(client):
    create_link(client, short_name="one")
    create_link(client, original_url="https://example.com/two", short_name="two")

    response = client.get("/api/links")

    assert response.status_code == 200
    assert response.headers["Accept-Ranges"] == "links"
    assert response.headers["Content-Range"] == "links 0-9/2"
    assert response.get_json() == [
        {
            "id": 1,
            "original_url": "https://example.com/long-url",
            "short_name": "one",
            "short_url": "http://localhost:8080/r/one",
        },
        {
            "id": 2,
            "original_url": "https://example.com/two",
            "short_name": "two",
            "short_url": "http://localhost:8080/r/two",
        },
    ]


def test_get_link(client):
    create_link(client)

    response = client.get("/api/links/1")

    assert response.status_code == 200
    assert response.get_json()["short_name"] == "exmpl"


def test_get_link_returns_404(client):
    response = client.get("/api/links/404")

    assert response.status_code == 404
    assert response.get_json() == {"error": "link not found"}


def test_update_link(client):
    create_link(client)

    response = client.put(
        "/api/links/1",
        json={"original_url": "https://hexlet.io", "short_name": "hexlet"},
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "id": 1,
        "original_url": "https://hexlet.io",
        "short_name": "hexlet",
        "short_url": "http://localhost:8080/r/hexlet",
    }


def test_update_link_returns_404(client):
    response = client.put(
        "/api/links/404",
        json={"original_url": "https://hexlet.io", "short_name": "hexlet"},
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "link not found"}


def test_update_link_rejects_duplicate_short_name(client):
    create_link(client, short_name="one")
    create_link(client, short_name="two")

    response = client.put(
        "/api/links/2",
        json={"original_url": "https://example.com/two", "short_name": "one"},
    )

    assert response.status_code == 409
    assert response.get_json() == {"error": "short_name already exists"}


def test_update_link_rejects_short_name_with_path_separator(client):
    create_link(client)

    response = client.put(
        "/api/links/1",
        json={"original_url": "https://hexlet.io", "short_name": "a/b"},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "short_name must not contain path separators"}


def test_delete_link(client):
    create_link(client)

    response = client.delete("/api/links/1")

    assert response.status_code == 204
    assert response.text == ""
    assert client.get("/api/links/1").status_code == 404


def test_delete_link_returns_404(client):
    response = client.delete("/api/links/404")

    assert response.status_code == 404
    assert response.get_json() == {"error": "link not found"}


def test_redirect_short_link(client):
    create_link(client)

    response = client.get("/r/exmpl", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"] == "https://example.com/long-url"


def test_list_links_supports_pagination(client):
    for index in range(12):
        create_link(
            client,
            original_url=f"https://example.com/{index}",
            short_name=f"link-{index}",
        )

    response = client.get("/api/links?range=[5,10]")

    assert response.status_code == 200
    assert response.headers["Content-Range"] == "links 5-10/12"
    assert [item["id"] for item in response.get_json()] == [6, 7, 8, 9, 10, 11]


def test_list_links_rejects_invalid_range(client):
    response = client.get("/api/links?range=bad")

    assert response.status_code == 400
    assert response.get_json() == {"error": "range must be a JSON array"}
