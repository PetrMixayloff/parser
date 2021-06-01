from fastapi import FastAPI
from app.config import settings
from app.api.endpoints import api_router

app = FastAPI(openapi_url=f"{settings.API_STR}/openapi.json")


app.include_router(api_router, prefix="")
