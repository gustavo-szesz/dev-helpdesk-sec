from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user, get_db

router = APIRouter()

@router.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, user=Depends(get_current_user), con=Depends(get_db)):
    ticket = con.execute(
        "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
    ).fetchone()
    if ticket is None:
        raise HTTPException(status_code=401)
    return dict(ticket)