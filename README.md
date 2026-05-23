# CleanLLM SaaS

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Mr-nishan/Clean_LLM_Pipeline)

Turn CSV **text** into **JSONL** training data — FastAPI app built for portfolio demos.

> **Live demo:** `https://YOUR-PROJECT.vercel.app`  
> Replace after deploy (Vercel → your project → Domains).

---

## About

1. Upload a CSV with a `text` column  
2. Dedupe, normalize, and clean each row  
3. Download JSONL (`prompt` / `response` pairs)

---

## Deploy on Vercel

1. Push this repo to GitHub.  
2. [vercel.com](https://vercel.com) → **Add New Project** → import repo.  
3. Leave defaults (Vercel detects `vercel.json` + `api/index.py`).  
4. **Deploy** → copy your `.vercel.app` URL into this README.

**Do not commit:** `venv/`, `.env`

**Note:** Free tier may be slow on first request (cold start). Uploads use `/tmp` on Vercel (files are temporary).

---

## Local development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open http://127.0.0.1:8000 — test with `app/data/sample-input.csv`.

---

## Sample downloads

| File | URL |
|------|-----|
| Input CSV | `/samples/input` |
| Output JSONL | `/samples/output` |

---

## API

| Method | Path |
|--------|------|
| `GET` | `/`, `/upload`, `/dashboard` |
| `POST` | `/process` (multipart `file`) |
| `GET` | `/download/{file_id}` |
| `GET` | `/health`, `/docs` |

---

## Project layout

```
api/index.py          # Vercel serverless entry (Mangum)
app/                  # FastAPI app + pipeline
app/data/             # Sample CSV + JSONL
public/static/css/    # Styles (CDN on Vercel)
vercel.json
requirements.txt
```

---

## Resume line

> **CleanLLM Pipeline** — [Live demo](https://YOUR-PROJECT.vercel.app) · FastAPI on Vercel · CSV → JSONL for LLM dataset prep
