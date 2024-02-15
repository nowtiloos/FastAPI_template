from fastapi import FastAPI
from app.api.users.router import router as router_user
from app.api.auth.router import router as router_auth

app: FastAPI = FastAPI()

app.include_router(router_auth)
app.include_router(router_user)
