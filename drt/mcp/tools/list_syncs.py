"""Implementation for the ``drt_list_syncs`` MCP tool.

Public docstring lives on the ``@mcp.tool()`` wrapper in
``drt/mcp/server.py`` — that's what MCP clients see; this is the extracted
logic, independently testable without constructing a server.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from drt.mcp._context import McpContext


def list_syncs(ctx: McpContext) -> list[dict[str, str]]:
    syncs = ctx.load_syncs()
    return [
        {
            "name": s.name,
            "description": s.description,
            "model": s.model,
            "destination_type": s.destination.type,
            "mode": s.sync.mode,
        }
        for s in syncs
    ]
