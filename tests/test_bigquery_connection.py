
"""Optional integration test for the BigQuery dataset."""

import os

import pytest
from google.cloud import bigquery

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "")
DATASET_ID = os.getenv("BIGQUERY_DATASET", "compass_mini")


@pytest.mark.skipif(
    os.getenv("RUN_BIGQUERY_INTEGRATION") != "1",
    reason="BigQuery integration test is opt-in; cloud credentials are required.",
)
def test_bigquery_dataset_connection():
    """Confirm the configured BigQuery dataset is accessible."""
    if not PROJECT_ID:
        pytest.fail("Set GOOGLE_CLOUD_PROJECT before running this integration test.")

    client = bigquery.Client(project=PROJECT_ID)
    dataset = client.get_dataset(f"{PROJECT_ID}.{DATASET_ID}")

    assert dataset.dataset_id == DATASET_ID
    assert dataset.location == "EU"
