
from google.cloud import bigquery

PROJECT_ID = "jaffle-shop-511913"
DATASET_ID = "compass_mini"


def test_bigquery_dataset_connection():
    client = bigquery.Client(project=PROJECT_ID)
    dataset = client.get_dataset(f"{PROJECT_ID}.{DATASET_ID}")

    assert dataset.dataset_id == DATASET_ID
    assert dataset.location == "EU"
