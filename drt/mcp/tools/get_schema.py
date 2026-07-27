"""Implementation for the ``drt_get_schema`` MCP tool.

Public docstring lives on the ``@mcp.tool()`` wrapper in
``drt/mcp/server.py``. Takes no context — the original tool never touched
``project_dir``.
"""

from __future__ import annotations

from typing import Any


def get_schema(schema_type: str = "sync") -> dict[str, Any]:
    from drt.config.schema import generate_project_schema, generate_sync_schema

    if schema_type == "project":
        return generate_project_schema()
    return generate_sync_schema()
