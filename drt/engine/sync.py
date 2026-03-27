"""Sync Engine — orchestrates extract → transform → load.

This module is the primary candidate for future Rust rewrite (PyO3).
Keep it pure: no I/O side effects beyond source/destination calls.
"""

from collections.abc import Iterator
from typing import Any

from drt.config.models import DestinationConfig, SourceConfig, SyncConfig
from drt.destinations.base import Destination, SyncResult
from drt.sources.base import Source


def batch(iterable: Iterator[Any], size: int) -> Iterator[list[Any]]:
    """Yield successive batches of `size` from an iterator."""
    chunk: list[Any] = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) >= size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def run_sync(
    sync: SyncConfig,
    source: Source,
    destination: Destination,
    source_config: SourceConfig,
    dry_run: bool = False,
) -> SyncResult:
    """Run a single sync: extract from source, load to destination."""
    # TODO: resolve model ref to actual SQL query (Phase 1)
    query = f"SELECT * FROM {sync.model}"

    records_iter = source.extract(query, source_config)
    total_result = SyncResult()

    for record_batch in batch(records_iter, sync.sync.batch_size):
        if dry_run:
            total_result.success += len(record_batch)
            continue
        result = destination.load(record_batch, sync.destination)
        total_result.success += result.success
        total_result.failed += result.failed
        total_result.skipped += result.skipped
        total_result.errors.extend(result.errors)

        if sync.sync.on_error == "fail" and result.failed > 0:
            break

    return total_result
