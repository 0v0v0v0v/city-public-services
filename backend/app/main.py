from contextlib import asynccontextmanager
from pathlib import Path
import socket

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.api.public import router as public_router
from app.core.config import settings
from app.db.init_db import init_db


BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIST_DIR = BASE_DIR / "frontend" / "dist"
FRONTEND_INDEX_FILE = FRONTEND_DIST_DIR / "index.html"
FRONTEND_DEV_URL = "http://127.0.0.1:5173"


def is_frontend_dev_server_running() -> bool:
    try:
        with socket.create_connection(("127.0.0.1", 5173), timeout=0.15):
            return True
    except OSError:
        return False


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public_router, prefix=settings.api_prefix)
app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(admin_router, prefix=settings.api_prefix)

if FRONTEND_DIST_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST_DIR / "assets"), name="assets")


@app.get("/healthz")
def health_check():
    return {"message": settings.app_name, "status": "ok"}


@app.get("/favicon.svg")
def favicon():
    if is_frontend_dev_server_running():
        return RedirectResponse(f"{FRONTEND_DEV_URL}/favicon.svg")
    if (FRONTEND_DIST_DIR / "favicon.svg").exists():
        return FileResponse(FRONTEND_DIST_DIR / "favicon.svg")
    return JSONResponse(status_code=404, content={"detail": "Not found."})


@app.get("/icons.svg")
def icons():
    if is_frontend_dev_server_running():
        return RedirectResponse(f"{FRONTEND_DEV_URL}/icons.svg")
    if (FRONTEND_DIST_DIR / "icons.svg").exists():
        return FileResponse(FRONTEND_DIST_DIR / "icons.svg")
    return JSONResponse(status_code=404, content={"detail": "Not found."})


@app.get("/{full_path:path}")
def serve_frontend(full_path: str):
    if full_path.startswith("api/"):
        return JSONResponse(status_code=404, content={"detail": "API endpoint not found."})

    if is_frontend_dev_server_running():
        target_path = full_path or ""
        suffix = f"/{target_path}" if target_path else ""
        return RedirectResponse(f"{FRONTEND_DEV_URL}{suffix}")

    if FRONTEND_INDEX_FILE.exists():
        requested_file = FRONTEND_DIST_DIR / full_path
        if full_path and requested_file.exists() and requested_file.is_file():
            return FileResponse(requested_file)
        return FileResponse(FRONTEND_INDEX_FILE)

    return JSONResponse(
        status_code=503,
        content={
            "detail": "Frontend build not found. Run `npm run build` in the frontend directory.",
        },
    )
