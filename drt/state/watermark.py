"""Watermark storage backends for incremental sync.

Provides pluggable storage for cursor/watermark values:
- LocalWatermarkStorage: file-based (.drt/watermarks.json)
- GCSWatermarkStorage: Google Cloud Storage blob
- BigQueryWatermarkStorage: BigQuery _drt_watermarks table
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol


class WatermarkStorage(Protocol):
    """Read and write watermark values for incremental syncs."""

    def get(self, sync_name: str) -> str | None: ...
    def save(self, sync_name: str, value: str) -> None: ...


class LocalWatermarkStorage:
    """File-based watermark storage using .drt/watermarks.json."""

    def __init__(self, project_dir: Path) -> None:
        self._state_dir = project_dir / ".drt"
        self._file = self._state_dir / "watermarks.json"

    def _load(self) -> dict[str, str]:
        if not self._file.exists():
            return {}
        try:
            with self._file.open() as f:
                data: dict[str, str] = json.load(f) or {}
                return data
        except (json.JSONDecodeError, ValueError):
            return {}

    def _save_all(self, data: dict[str, str]) -> None:
        self._state_dir.mkdir(exist_ok=True)
        with self._file.open("w") as f:
            json.dump(data, f, indent=2)

    def get(self, sync_name: str) -> str | None:
        return self._load().get(sync_name)

    def save(self, sync_name: str, value: str) -> None:
        data = self._load()
        data[sync_name] = value
        self._save_all(data)


def _gcs_client() -> Any:
    """Lazy GCS client — import only when needed."""
    try:
        from google.cloud import storage  # type: ignore[import-untyped]
    except ImportError as e:
        raise ImportError(
            "GCS watermark storage requires: pip install drt-core[gcs]"
        ) from e
    return storage.Client()


class GCSWatermarkStorage:
    """Google Cloud Storage watermark backend.

    Stores watermarks as a JSON object in a single GCS blob.
    """

    def __init__(self, bucket: str, key: str) -> None:
        self._bucket_name = bucket
        self._key = key

    def _blob(self) -> Any:
        client = _gcs_client()
        return client.bucket(self._bucket_name).blob(self._key)

    def _load(self) -> dict[str, str]:
        blob = self._blob()
        if not blob.exists():
            return {}
        try:
            data: dict[str, str] = json.loads(blob.download_as_text())
            return data
        except (json.JSONDecodeError, ValueError):
            return {}

    def get(self, sync_name: str) -> str | None:
        return self._load().get(sync_name)

    def save(self, sync_name: str, value: str) -> None:
        data = self._load()
        data[sync_name] = value
        self._blob().upload_from_string(
            json.dumps(data, indent=2), content_type="application/json",
        )
