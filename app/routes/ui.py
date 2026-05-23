from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.ui.layout import page

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home():
    content = """
    <section class="hero">
      <p class="hero__eyebrow">Dataset prep</p>
      <h1>Clean text. Export JSONL. Ship faster.</h1>
      <p class="hero__lead">
        Upload a CSV with a <code>text</code> column. We dedupe, normalize,
        and package prompt–response pairs you can drop into fine-tuning workflows.
      </p>
      <div class="hero__actions">
        <a class="btn btn--primary" href="/upload">Upload a CSV</a>
        <a class="btn btn--ghost" href="/dashboard">View past jobs</a>
      </div>
    </section>

    <section class="sample-downloads">
      <header class="page-head">
        <h2>Sample datasets</h2>
        <p>Download these to try the app or inspect the expected input/output format.</p>
      </header>
      <div class="grid-3">
        <article class="card">
          <h3>Input CSV</h3>
          <p>4 rows with a <code>text</code> column — use this on the Upload page.</p>
          <a class="btn btn--ghost" href="/samples/input" download>Download sample-input.csv</a>
        </article>
        <article class="card">
          <h3>Output JSONL</h3>
          <p>Result after cleaning — one JSON object per line (prompt + response).</p>
          <a class="btn btn--ghost" href="/samples/output" download>Download sample-output.jsonl</a>
        </article>
        <article class="card">
          <h3>API</h3>
          <p>Programmatic access and OpenAPI docs for integrations.</p>
          <a class="btn btn--ghost" href="/docs">Open API docs</a>
        </article>
      </div>
    </section>

    <div class="grid-3">
      <article class="card">
        <h3>1 · Upload</h3>
        <p>Drop a spreadsheet export. We only need one column named <strong>text</strong>.</p>
      </article>
      <article class="card">
        <h3>2 · Clean</h3>
        <p>Lowercase, strip noise, remove blanks and duplicate rows automatically.</p>
      </article>
      <article class="card">
        <h3>3 · Download</h3>
        <p>Grab a <strong>.jsonl</strong> file — one JSON object per line, ready for training pipelines.</p>
      </article>
    </div>
    """
    return page("Home", content, active="home")


@router.get("/upload", response_class=HTMLResponse)
def upload_page():
    content = """
    <header class="page-head">
      <h1>Upload your CSV</h1>
      <p>We’ll run the cleaning pipeline and give you a download link when it’s done. Usually takes a few seconds.</p>
    </header>

    <div class="upload-panel">
      <label class="dropzone" id="dropzone" for="file">
        <div class="dropzone__icon" aria-hidden="true">📄</div>
        <p class="dropzone__title">Drag & drop your file here</p>
        <p class="dropzone__hint">or click to browse — .csv only</p>
        <input type="file" id="file" accept=".csv,text/csv" />
      </label>

      <div class="file-chip" id="file-chip">
        <span aria-hidden="true">✓</span>
        <span class="file-chip__name" id="file-name"></span>
      </div>

      <div class="upload-actions">
        <button class="btn btn--primary" id="submit-btn" type="button" disabled>
          <span class="spinner" id="spinner" aria-hidden="true"></span>
          <span id="btn-label">Process dataset</span>
        </button>
      </div>

      <div class="requirements">
        <strong>Format:</strong> CSV with a header row and a column named <code>text</code>.
        Empty rows and duplicate entries are removed before export.
        <br><br>
        <strong>Try a sample:</strong>
        <a href="/samples/input" download>Download sample-input.csv</a>
        ·
        <a href="/samples/output" download>See sample-output.jsonl</a>
      </div>

      <div class="result" id="result" role="status" aria-live="polite"></div>
    </div>

    <script>
    (function () {
      const dropzone = document.getElementById("dropzone");
      const fileInput = document.getElementById("file");
      const fileChip = document.getElementById("file-chip");
      const fileName = document.getElementById("file-name");
      const submitBtn = document.getElementById("submit-btn");
      const spinner = document.getElementById("spinner");
      const btnLabel = document.getElementById("btn-label");
      const result = document.getElementById("result");

      function setFile(file) {
        if (!file) return;
        fileInput.files = createFileList(file);
        fileName.textContent = file.name;
        fileChip.classList.add("is-visible");
        submitBtn.disabled = false;
        result.classList.remove("is-visible", "result--error");
      }

      function createFileList(file) {
        const dt = new DataTransfer();
        dt.items.add(file);
        return dt.files;
      }

      fileInput.addEventListener("change", () => {
        if (fileInput.files[0]) setFile(fileInput.files[0]);
      });

      ["dragenter", "dragover"].forEach((evt) => {
        dropzone.addEventListener(evt, (e) => {
          e.preventDefault();
          dropzone.classList.add("is-dragover");
        });
      });

      ["dragleave", "drop"].forEach((evt) => {
        dropzone.addEventListener(evt, (e) => {
          e.preventDefault();
          dropzone.classList.remove("is-dragover");
        });
      });

      dropzone.addEventListener("drop", (e) => {
        const file = e.dataTransfer.files[0];
        if (file) setFile(file);
      });

      function setLoading(loading) {
        submitBtn.disabled = loading || !fileInput.files[0];
        spinner.classList.toggle("is-visible", loading);
        btnLabel.textContent = loading ? "Processing…" : "Process dataset";
      }

      submitBtn.addEventListener("click", async () => {
        const file = fileInput.files[0];
        if (!file) return;

        setLoading(true);
        result.classList.remove("is-visible", "result--error");

        const form = new FormData();
        form.append("file", file);

        async function parseResponse(res) {
          const text = await res.text();
          try {
            return JSON.parse(text);
          } catch {
            throw new Error(
              text.slice(0, 200) || ("Server error (" + res.status + ")")
            );
          }
        }

        try {
          const res = await fetch("/process", { method: "POST", body: form });
          const data = await parseResponse(res);

          if (!res.ok) {
            const msg = Array.isArray(data.detail)
              ? data.detail.map((d) => d.msg || d).join(", ")
              : (data.detail || data.error || "Upload failed");
            throw new Error(msg);
          }

          result.className = "result is-visible";
          result.innerHTML = `
            <h3>All set — your dataset is ready</h3>
            <div class="result-stats">
              <div class="stat">
                <span class="stat__value">${data.rows}</span>
                <span class="stat__label">Rows kept</span>
              </div>
              <div class="stat">
                <span class="stat__value">${data.pairs}</span>
                <span class="stat__label">Training pairs</span>
              </div>
            </div>
            <a class="btn btn--primary" href="${data.download_url}">Download JSONL</a>
          `;
        } catch (err) {
          result.className = "result result--error is-visible";
          result.innerHTML = `
            <h3>Something went wrong</h3>
            <p>${err.message || "Could not process this file. Check the format and try again."}</p>
          `;
        } finally {
          setLoading(false);
        }
      });
    })();
    </script>
    """
    return page("Upload", content, active="upload")
