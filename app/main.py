from fastapi import FastAPI
from app.users.router import router as router_user
from app.auth.router import router as router_auth

app = FastAPI()
app.include_router(router_auth)
app.include_router(router_user)
