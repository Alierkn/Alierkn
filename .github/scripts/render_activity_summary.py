from __future__ import annotations

import datetime as dt
import html
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


USERNAME = "Alierkn"
OUTPUT = Path("assets/activity-summary.svg")
FEATURED = [
    ("gromacs-mcp", "Scientific MCP", "Python / GROMACS"),
    ("vmd-mcp", "Molecular tooling", "Python / VMD"),
    ("boost", "macOS CLI", "Bash / gum"),
    ("claude-tracker", "Local-first extension", "JavaScript / MV3"),
    ("Data-Mining-Lesson-Unime", "University data", "Python / Jupyter"),
    ("edufrench", "Education product", "TypeScript / Next.js"),
]


def github_json(path: str) -> dict[str, Any] | None:
    token = os.environ.get("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Alierkn-profile-activity-summary",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
        return None


def format_date(value: str | None) -> str:
    if not value:
        return "active"
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.strftime("%b %d, %Y")


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def repo_rows(repos: list[dict[str, Any]]) -> str:
    rows = []
    for index, (name, role, stack) in enumerate(FEATURED):
        repo = next((item for item in repos if item.get("name") == name), {})
        updated = format_date(repo.get("pushed_at"))
        y = 310 + index * 24
        color = ["#38bdf8", "#818cf8", "#34d399", "#f59e0b", "#22c55e", "#60a5fa"][index]
        rows.append(
            f"""
    <g transform="translate(86 {y})">
      <circle cx="0" cy="8" r="4.5" fill="{color}"/>
      <text x="18" y="13" class="repo">{esc(name)}</text>
      <text x="310" y="13" class="muted">{esc(role)}</text>
      <text x="542" y="13" class="muted">{esc(stack)}</text>
      <text x="792" y="13" class="date">{esc(updated)}</text>
    </g>"""
        )
    return "".join(rows)


def render() -> str:
    repos = [github_json(f"/repos/{USERNAME}/{name}") or {"name": name} for name, _, _ in FEATURED]
    updated = dt.datetime.now(dt.UTC).strftime("%b %d, %Y")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="500" viewBox="0 0 1200 500" role="img" aria-labelledby="title desc">
  <title id="title">Activity and public work signals</title>
  <desc id="desc">A compact summary of Ali Erkan Ocakli's public GitHub activity and featured projects.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="52%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="48%" stop-color="#818cf8"/>
      <stop offset="100%" stop-color="#34d399"/>
    </linearGradient>
    <style>
      text {{ font-family: Arial, Helvetica, sans-serif; }}
      .title {{ fill: #f8fafc; font-size: 42px; font-weight: 800; }}
      .subtitle {{ fill: #cbd5e1; font-size: 18px; font-weight: 500; }}
      .label {{ fill: #94a3b8; font-size: 13px; font-weight: 700; letter-spacing: 1.2px; }}
      .value {{ fill: #f8fafc; font-size: 30px; font-weight: 800; }}
      .hint {{ fill: #94a3b8; font-size: 13px; font-weight: 600; }}
      .repo {{ fill: #e0f2fe; font-size: 14px; font-weight: 800; }}
      .muted {{ fill: #cbd5e1; font-size: 13px; font-weight: 600; }}
      .date {{ fill: #94a3b8; font-size: 13px; font-weight: 600; }}
    </style>
  </defs>
  <rect width="1200" height="500" rx="30" fill="url(#bg)"/>
  <rect x="44" y="44" width="1112" height="432" rx="24" fill="#020617" fill-opacity="0.58" stroke="#334155"/>
  <rect x="44" y="44" width="1112" height="5" rx="2.5" fill="url(#accent)"/>

  <text x="82" y="104" class="title">Activity &amp; Signals</text>
  <text x="82" y="136" class="subtitle">Public work snapshot for AI tooling, data systems, and developer products.</text>

  <g transform="translate(82 150)">
    <rect width="314" height="92" rx="18" fill="#0f172a" stroke="#1e293b"/>
    <text x="22" y="30" class="label">FEATURED SYSTEMS</text>
    <text x="22" y="63" class="value">{len(FEATURED)}</text>
    <text x="72" y="62" class="hint">MCP, CLI, extension, course</text>
  </g>
  <g transform="translate(442 150)">
    <rect width="314" height="92" rx="18" fill="#0f172a" stroke="#1e293b"/>
    <text x="22" y="30" class="label">CURATED REPOS</text>
    <text x="22" y="63" class="value">{len(FEATURED)}</text>
    <text x="72" y="62" class="hint">AI, data, developer tools</text>
  </g>
  <g transform="translate(802 150)">
    <rect width="314" height="92" rx="18" fill="#0f172a" stroke="#1e293b"/>
    <text x="22" y="30" class="label">MAINTENANCE LAYERS</text>
    <text x="22" y="63" class="value">3</text>
    <text x="72" y="62" class="hint">CI + security + deps</text>
  </g>

  <text x="82" y="286" class="label">FEATURED PUBLIC WORK</text>
  <text x="628" y="286" class="label">STACK</text>
  <text x="878" y="286" class="label">LAST PUSH</text>
  {repo_rows(repos)}

  <text x="82" y="466" class="date">Generated {esc(updated)} from public GitHub repository data.</text>
</svg>
"""


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
