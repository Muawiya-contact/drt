"""BigQuery source implementation.

Requires: pip install drt-core[bigquery]
"""

from collections.abc import Iterator

from drt.config.models import SourceConfig


class BigQuerySource:
    """Extract records from Google BigQuery."""

    def extract(self, query: str, config: SourceConfig) -> Iterator[dict]:
        """Run a SQL query and yield rows as dicts."""
        try:
            from google.cloud import bigquery  # type: ignore[import]
        except ImportError as e:
            raise ImportError(
                "BigQuery support requires: pip install drt-core[bigquery]"
            ) from e

        client = bigquery.Client(project=config.project)
        rows = client.query(query).result()
        for row in rows:
            yield dict(row)

    def test_connection(self, config: SourceConfig) -> bool:
        try:
            from google.cloud import bigquery  # type: ignore[import]

            client = bigquery.Client(project=config.project)
            client.query("SELECT 1").result()
            return True
        except Exception:
            return False
