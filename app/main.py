from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import dashboard, download, samples, ui, upload
from app.services.file_service import ensure_output_dir

PUBLIC_STATIC = Path(__file__).resolve().parent.parent / "public" / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_output_dir()
    yield


app = FastAPI(title="CleanLLM SaaS", lifespan=lifespan)

if PUBLIC_STATIC.is_dir():
    app.mount("/static", StaticFiles(directory=str(PUBLIC_STATIC)), name="static")

app.include_router(ui.router)
app.include_router(upload.router)
app.include_router(download.router)
app.include_router(samples.router)
app.include_router(dashboard.router)


@app.get("/health")
def health():
    return {"status": "ok"}
