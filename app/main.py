from fastapi import FastAPI

from app.api.routes import api_router
from app.core.errors import register_exception_handlers

app = FastAPI(
    title="Scalable Backend & API Platform",
    description="Portfolio sample: layered FastAPI backend with auth, validation, and tests.",
    version="1.0.0",
)

register_exception_handlers(app)
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
