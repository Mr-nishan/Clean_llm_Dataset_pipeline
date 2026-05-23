# routes/upload.py
from fastapi import APIRouter, File, HTTPException, UploadFile

import pandas as pd

from app.core.pipeline import run_pipeline
from app.exporter import export_jsonl
from app.services.file_service import ensure_output_dir, generate_file_id, get_output_path
from app.state.history import history_store

router = APIRouter()


@router.post("/process")
async def process(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        file_id = generate_file_id()
        output_path = get_output_path(file_id)

        df, dataset = run_pipeline(df)

        ensure_output_dir()
        export_jsonl(dataset, output_path)

        download_url = f"/download/{file_id}"
        history_store.append(
            {
                "filename": file.filename or "upload.csv",
                "rows": len(df),
                "pairs": len(dataset),
                "download_url": download_url,
            }
        )

        return {
            "file_id": file_id,
            "rows": len(df),
            "pairs": len(dataset),
            "download_url": download_url,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not process file: {exc}",
        ) from exc