from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user, get_db

router = APIRouter()


def can_read_ticket(user, ticket):
    if ticket["tenants_id"] != user["tenants_id"]:        
        return False
    if user["role"] in ("agent", "admin"):
        return True
    return ticket["author_id"] == user["id"]      


@router.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, user=Depends(get_current_user), con=Depends(get_db)):
    ticket = con.execute(
        "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
    ).fetchone()
    if ticket is None or not can_read_ticket(user, ticket):
        raise HTTPException(status_code=404)       
    return dict(ticket)