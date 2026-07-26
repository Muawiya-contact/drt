"""Implementation for the ``drt_list_connectors`` MCP tool.

Public docstring lives on the ``@mcp.tool()`` wrapper in
``drt/mcp/server.py``. Takes no context — the original tool never touched
``project_dir``.
"""

from __future__ import annotations


def list_connectors() -> dict[str, list[dict[str, str]]]:
    # Derived from the drt.config.connectors SSoT (kept in lockstep with
    # drt/connectors/registry.py by test_cli_list_connectors), so this
    # inventory can never fall out of sync with the registry.
    from drt.config.connectors import connector_inventory

    return connector_inventory()
