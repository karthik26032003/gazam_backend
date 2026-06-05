from fastapi import FastAPI
from routers.webhook import router as webhook_router


app = FastAPI(title="Gazam WhatsApp Bot")

app.include_router(webhook_router)


@app.get("/")
def health():
    return {"status": "ok", "service": "Gazam WhatsApp Bot"}
