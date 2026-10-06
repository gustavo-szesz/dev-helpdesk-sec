import pytest
import sqlite3
from app.db import connect, create_table


@pytest.fixture
def con():
    c = connect(":memory:")
    create_table(c)
    yield c
    c.close()


def test_tables_exist(con):
    lines = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    names = [line["name"] for line in lines]
    assert "tenants" in names
    assert "users" in names
    assert "tickets" in names


def test_user_without_tenant_is_blocked(con):
    with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY constraint failed"):
        con.execute(
            "INSERT INTO users (tenants_id, email, role) VALUES (999, 'a@b.com', 'client')"
        )


def test_invalid_role_is_blocked(con):
    con.execute("INSERT INTO tenants (name) VALUES ('empresa1')")
    with pytest.raises(sqlite3.IntegrityError, match="CHECK constraint failed"):
        con.execute(
            "INSERT INTO users (tenants_id, email, role) VALUES (1, 'a@b.com', 'hacker')"
        )


def test_invalid_status_is_blocked(con):
    con.execute("INSERT INTO tenants (name) VALUES ('empresa1')")
    con.execute(
        "INSERT INTO users (tenants_id, email, role) VALUES (1, 'a@b.com', 'client')"
    )
    with pytest.raises(sqlite3.IntegrityError, match="CHECK constraint failed"):
        con.execute(
            "INSERT INTO tickets (subject, description, tenants_id, author_id, status) "
            "VALUES ('assunto', 'descricao', 1, 1, 'qualquer_coisa')"
        )