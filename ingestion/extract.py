from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "sample"


def extract_grants() -> pd.DataFrame:
    """Read grant records from the sample CSV file."""
    file_path = DATA_DIR / "grants.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Grant file not found: {file_path}")

    return pd.read_csv(file_path)


def extract_payments() -> pd.DataFrame:
    """Read payment records from the sample CSV file."""
    file_path = DATA_DIR / "payments.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Payment file not found: {file_path}")

    return pd.read_csv(file_path)


if __name__ == "__main__":
    grants = extract_grants()
    payments = extract_payments()

    print(f"Extracted {len(grants)} grant records.")
    print(f"Extracted {len(payments)} payment records.")

    print("\nGrant sample:")
    print(grants.head())

    print("\nPayment sample:")
    print(payments.head())
