from fastapi import Depends, Header, HTTPException
from app.db import connect

def get_db():
    con = connect()
    try:
        yield con
    finally:
        con.close()

def get_current_user(x_user_id: int = Header(None), con=Depends(get_db)):
    if x_user_id is None:
        raise HTTPException(status_code=401)
    
    user  = con.execute(
        "SELECT * FROM users WHERE id = ?", (x_user_id,)
    ).fetchone()

    if user is None:
        raise HTTPException(status_code=401)

    return user
    