import os
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def _default_output_dir() -> Path:
    if os.environ.get("STORAGE_DIR"):
        return Path(os.environ["STORAGE_DIR"])
    if os.environ.get("VERCEL"):
        return Path("/tmp/cleanllm-outputs")
    return ROOT / "app" / "storage" / "outputs"


OUTPUT_DIR = _default_output_dir()


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_file_id() -> str:
    return str(uuid.uuid4())


def get_output_path(file_id: str) -> str:
    return str(OUTPUT_DIR / f"output_{file_id}.jsonl")
