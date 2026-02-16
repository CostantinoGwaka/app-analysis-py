from fastapi import FastAPI  # type: ignore
from app.api.analyze import router

app = FastAPI(title="Audit Intelligence Engine")

app.include_router(router, prefix="/api")
