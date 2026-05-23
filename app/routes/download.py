# routes/download.py
from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

from app.services.file_service import get_output_path

router = APIRouter()

@router.get("/download/{file_id}")
def download(file_id: str):

    path = get_output_path(file_id)

    if not os.path.exists(path):
        return {"error": "File not found"}

    return FileResponse(path, filename="dataset.jsonl")