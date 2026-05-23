from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import dashboard, download, samples, ui, upload
from app.services.file_service import ensure_output_dir

# Path to static files
PUBLIC_STATIC = Path(__file__).resolve().parent.parent / "public" / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Safe for local dev, but wrapped for Vercel safety
    try:
        ensure_output_dir()
    except Exception:
        pass  # Vercel filesystem may be read-only
    yield


app = FastAPI(title="CleanLLM SaaS", lifespan=lifespan)


# Mount static files only if directory exists
if PUBLIC_STATIC.exists() and PUBLIC_STATIC.is_dir():
    app.mount(
        "/static",
        StaticFiles(directory=str(PUBLIC_STATIC)),
        name="static"
    )


# Routers
app.include_router(ui.router)
app.include_router(upload.router)
app.include_router(download.router)
app.include_router(samples.router)
app.include_router(dashboard.router)


@app.get("/health")
def health():
    return {"status": "ok"}
