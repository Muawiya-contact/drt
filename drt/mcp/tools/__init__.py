"""Per-tool MCP implementation modules (#723 part 1).

Each module holds the plain, testable implementation for one
``@mcp.tool()`` — extracted from what used to be a single closure body in
``drt/mcp/server.py``. These are normal functions, not decorated: unlike
``drt/cli/commands/`` (which registers against one shared module-level
``app`` and can rely on import-time side effects), each MCP tool closes
over a ``project_dir`` that is per-``create_server()``-call, so the
``@mcp.tool()`` decoration itself stays in ``server.py`` as a thin wrapper
that imports and calls into the matching function here.

New tools should land here in their own module, taking an ``McpContext``
(``drt/mcp/_context.py``) as their first argument when they need
project/sync config, and be registered with a thin wrapper in
``drt/mcp/server.py``.
"""

from __future__ import annotations
