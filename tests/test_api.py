from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _login() -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "builder@example.com", "password": "demo-password"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_rejects_bad_password() -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "builder@example.com", "password": "wrong-password"},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


def test_create_and_list_projects() -> None:
    token = _login()
    headers = {"Authorization": f"Bearer {token}"}

    created = client.post(
        "/api/v1/projects",
        headers=headers,
        json={"name": "Mission API", "description": "Demo project"},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["name"] == "Mission API"
    assert body["status"] == "active"

    listed = client.get("/api/v1/projects", headers=headers)
    assert listed.status_code == 200
    assert any(item["id"] == body["id"] for item in listed.json())


def test_update_requires_auth() -> None:
    response = client.patch("/api/v1/projects/prj_missing", json={"status": "archived"})
    assert response.status_code == 401
