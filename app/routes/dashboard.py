from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.state.history import history_store
from app.ui.layout import page

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    if not history_store:
        content = """
        <header class="page-head">
          <h1>Your jobs</h1>
          <p>Every processed CSV shows up here with a quick download link.</p>
        </header>
        <div class="empty-state">
          <div class="empty-state__icon" aria-hidden="true">📂</div>
          <h2>No datasets yet</h2>
          <p>Upload a CSV to create your first JSONL export. It only takes a moment.</p>
          <a class="btn btn--primary" href="/upload">Upload a CSV</a>
        </div>
        """
        return page("Jobs", content, active="dashboard")

    rows = ""
    for h in reversed(history_store):
        rows += f"""
        <tr>
          <td>{h["filename"]}</td>
          <td>{h["rows"]}</td>
          <td>{h["pairs"]}</td>
          <td><a class="table-link" href="{h["download_url"]}">Download JSONL</a></td>
        </tr>
        """

    content = f"""
    <header class="page-head">
      <h1>Your jobs</h1>
      <p>{len(history_store)} dataset{"s" if len(history_store) != 1 else ""} processed this session.</p>
    </header>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>File</th>
            <th>Rows</th>
            <th>Pairs</th>
            <th>Export</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>
    <p style="margin-top:1.5rem;">
      <a class="btn btn--ghost" href="/upload">Process another file</a>
    </p>
    """
    return page("Jobs", content, active="dashboard")
