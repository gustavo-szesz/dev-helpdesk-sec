import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.auth import get_db
from modules.a01_access_control.fixed import router

@pytest.fixture
def client(con, ids):
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db] = lambda: con
    return TestClient(app)


def read_ticket(client, user_id, ticket_id):
    return client.get(
        f"/tickets/{ticket_id}",
        headers={"X-User-Id": str(user_id)},
    )


def test_client_cannot_read_other_tenant_ticket(client, ids):
    r = read_ticket(client, user_id=ids["client1"], ticket_id=ids["ticket2"])
    assert r.status_code in (403, 404)
    assert "subject" not in r.json()


def test_agent_cannot_read_other_tenant_ticket(client, ids):
    r = read_ticket(client, user_id=ids["agent1"], ticket_id=ids["ticket2"])
    assert r.status_code in (403, 404)


def test_client_can_read_own_ticket(client, ids):
    r = read_ticket(client, user_id=ids["client2"], ticket_id=ids["ticket2"])
    assert r.status_code == 200