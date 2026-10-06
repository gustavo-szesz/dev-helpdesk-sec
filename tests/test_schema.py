import pytest
import sqlite3
from app.db import connect, create_table
from app.seed import seed


def test_tables_exist(con):
    tables = {
        row["name"]
        for row in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    }
    assert {"tenants", "users", "tickets"} <= tables


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

def test_seed_creates_scenario(con):
    ids = seed(con)
    assert con.execute("SELECT COUNT(*) FROM tenants").fetchone()[0] == 2    # 6
    assert con.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 4      # 7
    assert con.execute("SELECT COUNT(*) FROM tickets").fetchone()[0] == 2    

    ticket = con.execute(
        "SELECT * FROM tickets WHERE id = ?", (ids["ticket2"],)
    ).fetchone()
    assert ticket["tenants_id"] == ids["t2"]
    assert ticket["author_id"] == ids["client2"]  