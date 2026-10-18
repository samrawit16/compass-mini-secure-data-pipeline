from ingestion.extract import extract_grants, extract_payments
from ingestion.validate import validate_grants, validate_payments
from ingestion.load import load_data, verify_data
from ingestion.bigquery_load import load_dataframe, verify_bigquery_data
def main() -> None:
    # 1. Extract
    grants = extract_grants()
    payments = extract_payments()
    print(f"Extracted {len(grants)} grants and {len(payments)} payments.")

    # 2. Validate
    validate_grants(grants)
    validate_payments(payments, grants)
    print("Data validation passed.")

    # 3. Load
    load_data(grants, payments)

    
    # 4. Verify SQLite
    verify_data()

    # 5. Load to BigQuery
    print("Loading data to BigQuery...")
    
    load_dataframe(grants, "grants")
    load_dataframe(payments, "payments")

    # 6. Verify BigQuery
    verify_bigquery_data(expected_rows=5)

    print("Pipeline completed successfully.")




if __name__ == "__main__":
    main()
