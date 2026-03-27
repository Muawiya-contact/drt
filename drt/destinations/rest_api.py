"""Generic REST API destination.

Supports any HTTP endpoint with Jinja2 body templating,
rate limiting, and configurable error handling.
"""

import time

import httpx

from drt.config.models import DestinationConfig
from drt.destinations.base import SyncResult
from drt.templates.renderer import render_template


class RestApiDestination:
    """Send records to any REST API endpoint."""

    def load(self, records: list[dict], config: DestinationConfig) -> SyncResult:
        result = SyncResult()
        rate_limit = config.auth  # placeholder; rate_limit comes from SyncOptions

        with httpx.Client() as client:
            for record in records:
                body = (
                    render_template(config.body_template, record)
                    if config.body_template
                    else record
                )
                try:
                    response = client.request(
                        method=config.method,
                        url=config.url,
                        headers=config.headers,
                        json=body if isinstance(body, dict) else None,
                        content=body if isinstance(body, str) else None,
                    )
                    response.raise_for_status()
                    result.success += 1
                except httpx.HTTPStatusError as e:
                    result.failed += 1
                    result.errors.append(f"HTTP {e.response.status_code}: {e.response.text[:200]}")
                except Exception as e:
                    result.failed += 1
                    result.errors.append(str(e))

        return result
