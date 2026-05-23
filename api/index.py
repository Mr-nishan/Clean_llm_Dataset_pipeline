"""Vercel serverless entrypoint for FastAPI."""

import os

from mangum import Mangum

from app.main import app
from app.services.file_service import ensure_output_dir

os.environ.setdefault("VERCEL", "1")
ensure_output_dir()

handler = Mangum(app, lifespan="off")
