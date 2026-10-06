from __future__ import annotations

from typing import TypedDict

class SeedIds(TypedDict):
    t1:      int
    t2:      int
    agent1:  int 
    client1: int
    agent2:  int
    client2: int
    ticket1: int 
    ticket2: int


def create_tenant(con, name: str) -> int:
    cur = con.execute("INSERT INTO tenants (name) VALUES (?)", (name,))
    return cur.lastrowid


def create_user(con, tenants_id: int, email: str, role: str) -> int:
    cur = con.execute(
        "INSERT INTO users (tenants_id, email, role) VALUES (?, ?, ?)",     
        (tenants_id, email, role,),                                         
    )
    return cur.lastrowid

def create_ticket(
    con, 
    tenants_id: int,
    author_id: int, 
    subject: str,
    description: str, 
    status: str = "open"):
    cur = con.execute(
        "INSERT INTO tickets (tenants_id, author_id, subject, description, status) VALUES (?, ?, ?, ?, ?)",
        (tenants_id, author_id, subject, description, status)
    )
    return cur.lastrowid
    
def seed(con) -> SeedIds:
    t1 = create_tenant(con, "empresa1")
    t2 = create_tenant(con, "empresa2")

    agent1 = create_user(con, t1, "agent1@empresa1.com", "agent")
    client1 = create_user(con, t1, "client1@empresa1.com", "client")
    agent2 = create_user(con, t2, "agent2@empresa2.com", "agent")
    client2 = create_user(con, t2, "client2@empresa2.com", "client")

    ticket1 = create_ticket(con, t1, client1, "Problema 1", "Descricao 1")
    ticket2 = create_ticket(con, t2, client2, "Problema 2", "Descricao 2")

    con.commit()

    return {
        "t1": t1,
        "t2": t2,
        "agent1": agent1,
        "client1": client1,
        "agent2": agent2,
        "client2": client2,
        "ticket1": ticket1,
        "ticket2": ticket2,
    }