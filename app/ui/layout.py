def page(title: str, content: str, active: str | None = None) -> str:
    nav_items = [
        ("home", "/", "Home"),
        ("upload", "/upload", "Upload"),
        ("dashboard", "/dashboard", "Jobs"),
    ]

    nav_html = ""
    for key, href, label in nav_items:
        cls = ' class="is-active"' if active == key else ""
        nav_html += f'<a href="{href}"{cls}>{label}</a>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · CleanLLM</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/static/css/main.css">
</head>
<body>
  <header class="site-header">
    <div class="site-header__inner">
      <a class="brand" href="/">
        <span class="brand__mark">C</span>
        <span class="brand__text">CleanLLM</span>
      </a>
      <nav class="nav" aria-label="Main">
        {nav_html}
      </nav>
    </div>
  </header>

  <main>
    {content}
  </main>

  <footer class="site-footer">
  Turn messy CSV text into training-ready JSONL — built for small teams prepping LLM datasets.
  </footer>
</body>
</html>"""
