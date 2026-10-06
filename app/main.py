from fastapi import FastAPI, Depends
from app.auth import get_current_user 

app = FastAPI()

@app.get("/health")
async def root():
    return {"status":"ok"}

@app.get("/me")
def me(user=Depends(get_current_user)):
    return dict(user)