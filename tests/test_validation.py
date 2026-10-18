import pandas as pd
import pytest

from ingestion.validate import validate_grants, validate_payments


@pytest.fixture
def grants():
    return pd.DataFrame({
        "grant_id": ["G001", "G002"],
        "organization": ["Green Future", "Health Network"],
        "program": ["Climate", "Health"],
        "grant_amount": [50000, 30000],
        "status": ["approved", "pending"],
    })


@pytest.fixture
def payments():
    return pd.DataFrame({
        "payment_id": ["P001", "P002"],
        "grant_id": ["G001", "G002"],
        "payment_date": ["2026-09-01", "2026-10-01"],
        "amount": [20000, 10000],
        "status": ["paid", "paid"],
    })


def test_valid_grants_pass(grants):
    validate_grants(grants)


def test_duplicate_grant_ids_fail(grants):
    grants.loc[1, "grant_id"] = "G001"
    with pytest.raises(ValueError, match="unique"):
        validate_grants(grants)


def test_negative_grant_amount_fails(grants):
    grants.loc[0, "grant_amount"] = -100
    with pytest.raises(ValueError, match="positive"):
        validate_grants(grants)


def test_valid_payments_pass(payments, grants):
    validate_payments(payments, grants)


def test_payment_with_unknown_grant_fails(payments, grants):
    payments.loc[0, "grant_id"] = "G999"
    with pytest.raises(ValueError, match="unknown grants"):
        validate_payments(payments, grants)


def test_invalid_payment_date_fails(payments, grants):
    payments.loc[0, "payment_date"] = "not-a-date"
    with pytest.raises(ValueError, match="valid"):
        validate_payments(payments, grants)


def test_negative_payment_amount_fails(payments, grants):
    payments.loc[0, "amount"] = -10
    with pytest.raises(ValueError, match="positive"):
        validate_payments(payments, grants)
