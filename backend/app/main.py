# File: main.py
# FastAPI application entrypoint. Assembles the middleware stack, registers
# all route modules under their respective URL prefixes, and orchestrates
# startup tasks (database initialisation + seeding of default roles/users).
# This is the top-level glue layer of the project architecture.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analytics, auth, documents, search, tasks
from app.core.config import settings
from app.db.session import init_db
from app.services.bootstrap import seed_defaults

app = FastAPI(title="AI Task & Knowledge Management API", version="1.0.0")

# CORS configuration — allows the frontend dev server to communicate
# with the backend during development without same-origin policy errors.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register domain-specific routers under logical URL prefixes.
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])


@app.on_event("startup")
def on_startup() -> None:
    # Initialises the database schema and seeds default admin/user roles and accounts.
    init_db()
    seed_defaults()


@app.get("/")
def root() -> dict[str, str]:
    # Health-check endpoint used by load balancers or monitoring tools.
    return {"status": "ok"}
