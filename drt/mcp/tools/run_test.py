"""Implementation for the ``drt_run_test`` MCP tool.

Public docstring lives on the ``@mcp.tool()`` wrapper in
``drt/mcp/server.py``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from drt.cli.commands.test import _SyncTestResult
    from drt.mcp._context import McpContext


def run_test(ctx: McpContext, sync_name: str | None = None) -> dict[str, Any]:
    # #851: the per-test loop (connect, build query, execute, check,
    # severity, error handling) lives in exactly one place —
    # `execute_tests_for_sync`, which `drt test` and `drt build` already
    # share. Re-implementing it here is how #400 happened. This tool is now
    # only the selection + envelope around it.
    from drt.cli.commands.test import execute_tests_for_sync

    syncs = ctx.load_syncs()
    if not syncs:
        return {"status": "no_syncs", "results": []}

    if sync_name is not None:
        syncs = [s for s in syncs if s.name == sync_name]
        if not syncs:
            return {"error": f"No sync named '{sync_name}' found."}

    syncs_with_tests = [s for s in syncs if s.tests]
    if not syncs_with_tests:
        return {"status": "no_tests", "results": []}

    had_failures = False
    results: list[_SyncTestResult] = []

    for sync in syncs_with_tests:
        sync_result, sync_failed = execute_tests_for_sync(
            sync,
            dry_run=False,
            # An MCP tool returns structured data over the transport and has
            # never printed to the console; `json_mode` alone already
            # silences it, and `quiet` keeps that true if the two ever come
            # apart.
            json_mode=True,
            quiet=True,
            # `--store-failures` writes .drt/test_failures/… on disk, and MCP
            # exposes no way to read a written sample back — nothing would
            # ever consume it (#851).
            store_failures=False,
        )
        results.append(sync_result)
        if sync_failed:
            had_failures = True

    return {
        "status": "failed" if had_failures else "passed",
        "results": results,
    }
