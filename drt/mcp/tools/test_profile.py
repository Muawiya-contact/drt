"""Implementation for the ``drt_test_profile`` MCP tool.

Public docstring lives on the ``@mcp.tool()`` wrapper in
``drt/mcp/server.py``. Takes no context — the original tool never touched
``project_dir``.
"""

from __future__ import annotations

from typing import Any


def test_profile(name: str) -> dict[str, Any]:
    from drt.config.credentials import load_profile
    from drt.connectors.registry import get_source

    try:
        profile = load_profile(name)
    except (FileNotFoundError, KeyError, ValueError) as e:
        return {"name": name, "ok": False, "error": str(e)}

    source = get_source(profile)
    try:
        ok = source.test_connection(profile)
    except Exception as e:
        return {"name": name, "type": profile.type, "ok": False, "error": str(e)}

    return {"name": name, "type": profile.type, "ok": bool(ok)}
