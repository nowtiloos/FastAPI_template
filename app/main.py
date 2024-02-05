from fastapi import FastAPI
from app.users.router import router as router_users
from app.auth.router import router as router_auth

app = FastAPI()
app.include_router(router_auth)
app.include_router(router_users)
