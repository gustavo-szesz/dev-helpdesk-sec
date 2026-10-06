import sqlite3

database = 'dev-base.db'
sql_statements = [
    """CREATE TABLE IF NOT EXISTS tenants (
        id INTEGER PRIMARY KEY,
        name text NOT NULL UNIQUE
    );""",

    """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, 
        tenants_id INTEGER NOT NULL,
        email text NOT NULL, 
        role  text NOT NULl CHECK (role IN ('client','agent','admin')),
        FOREIGN KEY (tenants_id) REFERENCES tenants (id)
    );""",
    """CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY, 
        subject text NOT NULL, 
        description text NOT NULL,
        tenants_id INTEGER NOT NULL,
        author_id INTEGER NOT NULL,   
        status TEXT NOT NULL CHECK (status IN ('open','in_progress', 'closed')), 
        FOREIGN KEY (tenants_id) REFERENCES tenants (id),
        FOREIGN KEY (author_id) REFERENCES users(id)
    );
    """
]

def connect(path: str = database):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con

def create_table(con):
    for command in sql_statements:
        con.execute(command)
    con.commit()