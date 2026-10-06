

def create_tenant(con, name):
    cur = con.execute("INSERT INTO tenants (name) VALUES (?)", (name,))
    return cur.lastrowid


def create_user(con, tenants_id, email, role):
    cur = con.execute(
        "INSERT INTO users (tenants_id, email, role) VALUES (?, ?, ?)",     
        (tenants_id, email, role,),                                         
    )
    return cur.lastrowid

def create_ticket(con, tenants_id, author_id, subject, description, status="open"):
    cur = con.execute(
        "INSERT INTO tickets (tenants_id, author_id, subject, description, status) VALUES (?, ?, ?, ?, ?)",
        (tenants_id, author_id, subject, description, status)
    )
    return cur.lastrowid