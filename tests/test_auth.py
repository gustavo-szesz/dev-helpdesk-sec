import pytest

from fastapi.testclient import TestClient 
from app.main import app
from app.auth import get_db


@pytest.fixture
def client(con, ids):
    app.dependency_overrides[get_db] = lambda: con
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_without_header_is_401(client):
    r = client.get("/me")
    assert r.status_code == 401

def test_unknown_user_is_401(client):
    r = client.get("/me", headers={"X-User-Id":"999"})
    assert r.status_code == 401

def test_valid_user_returns_200(client, ids):
    r = client.get("/me", headers={"X-User-Id": str(ids["client1"])})
    assert r.status_code == 200
    assert r.json()["email"] == 'client1@empresa1.com'