from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analytics, auth, documents, search, tasks
from app.core.config import settings
from app.db.session import init_db
from app.services.bootstrap import seed_defaults

app = FastAPI(title="AI Task & Knowledge Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    seed_defaults()


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok"}
