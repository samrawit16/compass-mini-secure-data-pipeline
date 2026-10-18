import pandas as pd


def validate_grants(grants: pd.DataFrame) -> None:
    """Validate grant records before loading."""

    required_columns = {
        "grant_id",
        "organization",
        "program",
        "grant_amount",
        "status",
    }

    missing = required_columns - set(grants.columns)
    if missing:
        raise ValueError(f"Grant columns missing: {sorted(missing)}")

    if grants["grant_id"].isna().any():
        raise ValueError("Grant IDs cannot be missing.")

    if grants["grant_id"].duplicated().any():
        raise ValueError("Grant IDs must be unique.")

    amounts = pd.to_numeric(grants["grant_amount"], errors="coerce")
    if amounts.isna().any() or (amounts <= 0).any():
        raise ValueError("Grant amounts must be positive numbers.")

    allowed_statuses = {"approved", "pending", "rejected"}
    if not set(grants["status"].dropna()).issubset(allowed_statuses):
        raise ValueError("Grant status contains an unsupported value.")

    if grants["status"].isna().any():
        raise ValueError("Grant status cannot be missing.")


def validate_payments(
    payments: pd.DataFrame,
    grants: pd.DataFrame,
) -> None:
    """Validate payment records and their grant references."""

    required_columns = {
        "payment_id",
        "grant_id",
        "payment_date",
        "amount",
        "status",
    }

    missing = required_columns - set(payments.columns)
    if missing:
        raise ValueError(f"Payment columns missing: {sorted(missing)}")

    if payments["payment_id"].isna().any():
        raise ValueError("Payment IDs cannot be missing.")

    if payments["payment_id"].duplicated().any():
        raise ValueError("Payment IDs must be unique.")

    amounts = pd.to_numeric(payments["amount"], errors="coerce")
    if amounts.isna().any() or (amounts <= 0).any():
        raise ValueError("Payment amounts must be positive numbers.")

    dates = pd.to_datetime(
        payments["payment_date"],
        format="%Y-%m-%d",
        errors="coerce",
    )
    if dates.isna().any():
        raise ValueError("Payment dates must be valid.")

    if payments["grant_id"].isna().any():
        raise ValueError("Payment grant IDs cannot be missing.")

    known_grants = set(grants["grant_id"])
    unknown_grants = set(payments["grant_id"]) - known_grants

    if unknown_grants:
        raise ValueError(
            f"Payments reference unknown grants: {sorted(unknown_grants)}"
        )

    allowed_statuses = {"paid", "pending", "failed", "refunded"}
    if payments["status"].isna().any():
        raise ValueError("Payment status cannot be missing.")

    if not set(payments["status"]).issubset(allowed_statuses):
        raise ValueError("Payment status contains an unsupported value.")
