"""Implementation for the ``drt_dlq`` MCP tool.

Public docstring lives on the ``@mcp.tool()`` wrapper in
``drt/mcp/server.py``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from drt.mcp._context import McpContext


def dlq(ctx: McpContext, sync_name: str | None = None, limit: int = 20) -> dict[str, Any]:
    from dataclasses import asdict

    from drt.state.dlq import DlqStore

    store = DlqStore(ctx.project_dir)
    if sync_name is None:
        return {"depths": store.all_depths()}

    depth = store.depth(sync_name)
    records = [asdict(e) for e in store.read(sync_name)[:limit]]
    return {
        "sync_name": sync_name,
        "depth": depth,
        "records": records,
        "truncated": depth > len(records),
    }
