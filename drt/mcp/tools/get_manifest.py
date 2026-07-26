"""Implementation for the ``drt_get_manifest`` MCP tool.

Public docstring lives on the ``@mcp.tool()`` wrapper in
``drt/mcp/server.py``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from drt.mcp._context import McpContext


def get_manifest(
    ctx: McpContext,
    include_state: bool = False,
    full_labels: bool = False,
    history_depth: int = 10,
) -> dict[str, Any]:
    from drt.docs.builder import build_manifest

    return build_manifest(
        ctx.project_dir,
        include_state=include_state,
        full_labels=full_labels,
        history_depth=history_depth,
    ).to_dict()
