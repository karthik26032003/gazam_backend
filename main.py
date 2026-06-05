import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.webhook import router as webhook_router
from database import create_tables

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="Gazam WhatsApp Bot", lifespan=lifespan)

app.include_router(webhook_router)


@app.get("/")
def health():
    return {"status": "ok", "service": "Gazam WhatsApp Bot"}
