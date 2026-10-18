
"""Load validated Compass Mini data into BigQuery."""

from google.cloud import bigquery

PROJECT_ID = "jaffle-shop-511913"
DATASET_ID = "compass_mini"


def load_dataframe(dataframe, table_name: str) -> int:
    """Load a DataFrame into BigQuery and return its row count."""
    if not table_name.replace("_", "").isalnum():
        raise ValueError("Invalid table name")

    if dataframe.empty:
        raise ValueError("Refusing to load an empty DataFrame")

    client = bigquery.Client(project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_EMPTY,
    )

    job = client.load_table_from_dataframe(
        dataframe,
        table_id,
        job_config=job_config,
        location="EU",
    )
    job.result()

    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows into {table_id}")
    return table.num_rows


def verify_bigquery_data(expected_rows: int = 5) -> None:
    """Verify row counts in the BigQuery grants and payments tables."""
    client = bigquery.Client(project=PROJECT_ID)

    for table_name in ("grants", "payments"):
        table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
        table = client.get_table(table_id)

        print(f"BigQuery {table_name}: {table.num_rows} rows")

        if table.num_rows != expected_rows:
            raise ValueError(
                f"Expected {expected_rows} rows in {table_name}, "
                f"but found {table.num_rows}"
            )

    print("BigQuery row-count verification passed.")

