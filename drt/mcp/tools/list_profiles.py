"""Implementation for the ``drt_list_profiles`` MCP tool.

Public docstring lives on the ``@mcp.tool()`` wrapper in
``drt/mcp/server.py``. Takes no context — the original tool never touched
``project_dir``.
"""

from __future__ import annotations

from typing import Any


def list_profiles() -> dict[str, Any]:
    from drt.config.credentials import load_raw_profiles

    profiles = load_raw_profiles()
    return {
        "profiles": [
            {"name": name, "type": (raw.get("type") if isinstance(raw, dict) else None)}
            for name, raw in profiles.items()
        ]
    }
