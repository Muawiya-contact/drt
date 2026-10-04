"""Build and serve the deterministic docs-demo fixture for Playwright."""

from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from drt.docs.builder import build_manifest, collect_sync_yaml_texts
from drt.docs.html import render_html

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "docs-demo"
SITE = ROOT / "test-results" / "docs-site"


def main() -> None:
    """Regenerate the fixture and serve it on Playwright's fixed local port."""
    manifest = build_manifest(FIXTURE, include_state=True)
    sync_yaml_texts = collect_sync_yaml_texts(FIXTURE)
    render_html(manifest, SITE, sync_yaml_texts=sync_yaml_texts)

    handler = partial(SimpleHTTPRequestHandler, directory=str(SITE))
    server = ThreadingHTTPServer(("127.0.0.1", 4173), handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
