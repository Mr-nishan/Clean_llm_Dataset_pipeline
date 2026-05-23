from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "data"

SAMPLE_FILES = {
    "input": ("sample-input.csv", "sample-input.csv", "text/csv"),
    "output": ("sample-output.jsonl", "sample-output.jsonl", "application/jsonl"),
}


@router.get("/samples")
def samples_index():
    return {
        "input_csv": "/samples/input",
        "output_jsonl": "/samples/output",
    }


@router.get("/samples/input")
def download_sample_input():
    path, name, media = _resolve("input")
    return FileResponse(path, filename=name, media_type=media)


@router.get("/samples/output")
def download_sample_output():
    path, name, media = _resolve("output")
    return FileResponse(path, filename=name, media_type=media)


def _resolve(key: str) -> tuple[Path, str, str]:
    filename, download_name, media_type = SAMPLE_FILES[key]
    path = SAMPLES_DIR / filename
    if not path.is_file():
        raise HTTPException(status_code=404, detail=f"Sample file missing: {filename}")
    return path, download_name, media_type
