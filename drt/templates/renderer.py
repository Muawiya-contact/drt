"""Template renderer using Jinja2.

Future: replace with MiniJinja (Rust) via PyO3 for zero-dependency binary.
Interface is intentionally simple to make the swap transparent.
"""

from typing import Any

from jinja2 import BaseLoader, Environment, StrictUndefined
from jinja2.exceptions import UndefinedError


def render_template(template_str: str, row: dict[str, Any]) -> str:
    """Render a Jinja2 template string with a single row of data.

    Variables are accessed as {{ row.field_name }}.
    Raises ValueError on missing variables (strict mode).
    """
    env = Environment(loader=BaseLoader(), undefined=StrictUndefined)
    try:
        tmpl = env.from_string(template_str)
        return tmpl.render(row=row)
    except UndefinedError as e:
        raise ValueError(f"Template error: {e}") from e
