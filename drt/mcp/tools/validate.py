"""Implementation for the ``drt_validate`` MCP tool.

Public docstring lives on the ``@mcp.tool()`` wrapper in
``drt/mcp/server.py``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from drt.mcp._context import McpContext


def validate(ctx: McpContext) -> dict[str, Any]:
    result = ctx.load_syncs_safe()
    return {
        "valid": [s.name for s in result.syncs],
        "errors": result.errors,
    }
