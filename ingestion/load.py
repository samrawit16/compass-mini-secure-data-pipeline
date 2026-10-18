import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "compass.db"


def load_data(
    grants: pd.DataFrame,
    payments: pd.DataFrame,
) -> None:
    """Load validated grant and payment records into SQLite."""

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        grants.to_sql(
            "raw_grants",
            connection,
            if_exists="replace",
            index=False,
        )

        payments.to_sql(
            "raw_payments",
            connection,
            if_exists="replace",
            index=False,
        )

    print(f"Loaded {len(grants)} grants into raw_grants.")
    print(f"Loaded {len(payments)} payments into raw_payments.")
    print(f"Database location: {DB_PATH}")


def verify_data() -> None:
    """Report how many records are stored in each table."""

    with sqlite3.connect(DB_PATH) as connection:
        grants_count = pd.read_sql_query(
            "SELECT COUNT(*) AS total FROM raw_grants",
            connection,
        ).iloc[0]["total"]

        payments_count = pd.read_sql_query(
            "SELECT COUNT(*) AS total FROM raw_payments",
            connection,
        ).iloc[0]["total"]

    print(f"Verified database records: {grants_count} grants.")
    print(f"Verified database records: {payments_count} payments.")
