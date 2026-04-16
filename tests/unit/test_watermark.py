"""Tests for watermark storage backends."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from drt.state.watermark import LocalWatermarkStorage


class TestLocalWatermarkStorage:
    def test_get_returns_none_when_no_state(self, tmp_path: Path) -> None:
        storage = LocalWatermarkStorage(tmp_path)
        assert storage.get("my_sync") is None

    def test_save_and_get_round_trip(self, tmp_path: Path) -> None:
        storage = LocalWatermarkStorage(tmp_path)
        storage.save("my_sync", "2026-04-15T10:00:00")
        assert storage.get("my_sync") == "2026-04-15T10:00:00"

    def test_save_overwrites_previous(self, tmp_path: Path) -> None:
        storage = LocalWatermarkStorage(tmp_path)
        storage.save("my_sync", "old")
        storage.save("my_sync", "new")
        assert storage.get("my_sync") == "new"

    def test_independent_sync_names(self, tmp_path: Path) -> None:
        storage = LocalWatermarkStorage(tmp_path)
        storage.save("sync_a", "value_a")
        storage.save("sync_b", "value_b")
        assert storage.get("sync_a") == "value_a"
        assert storage.get("sync_b") == "value_b"


class TestGCSWatermarkStorage:
    @patch("drt.state.watermark._gcs_client")
    def test_get_returns_none_when_blob_missing(
        self, mock_client: MagicMock,
    ) -> None:
        from drt.state.watermark import GCSWatermarkStorage

        bucket = mock_client.return_value.bucket.return_value
        blob = bucket.blob.return_value
        blob.exists.return_value = False

        storage = GCSWatermarkStorage(
            bucket="my-bucket", key="watermarks/sync.json",
        )
        assert storage.get("my_sync") is None

    @patch("drt.state.watermark._gcs_client")
    def test_save_uploads_json(self, mock_client: MagicMock) -> None:
        from drt.state.watermark import GCSWatermarkStorage

        bucket = mock_client.return_value.bucket.return_value
        blob = bucket.blob.return_value
        blob.exists.return_value = False

        storage = GCSWatermarkStorage(
            bucket="my-bucket", key="watermarks/sync.json",
        )
        storage.save("my_sync", "2026-04-15T10:00:00")

        call_args = blob.upload_from_string.call_args
        uploaded = json.loads(call_args[0][0])
        assert uploaded["my_sync"] == "2026-04-15T10:00:00"

    @patch("drt.state.watermark._gcs_client")
    def test_get_reads_existing_blob(self, mock_client: MagicMock) -> None:
        from drt.state.watermark import GCSWatermarkStorage

        bucket = mock_client.return_value.bucket.return_value
        blob = bucket.blob.return_value
        blob.exists.return_value = True
        blob.download_as_text.return_value = '{"my_sync": "2026-04-15"}'

        storage = GCSWatermarkStorage(
            bucket="my-bucket", key="watermarks/sync.json",
        )
        assert storage.get("my_sync") == "2026-04-15"
