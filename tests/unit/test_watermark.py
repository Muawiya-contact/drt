"""Tests for watermark storage backends."""
from __future__ import annotations

from pathlib import Path

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
