
import pandas as pd

from src.reconciliation.run_reconciliation import run_reconciliation


def test_run_reconciliation(tmp_path, monkeypatch):
    # Create temporary project directories
    agency_a_dir = tmp_path / "data" / "silver" / "agency_a"
    agency_b_dir = tmp_path / "data" / "silver" / "agency_b"

    agency_a_dir.mkdir(parents=True)
    agency_b_dir.mkdir(parents=True)

    # Create sample Agency A data
    agency_a = pd.DataFrame({
        "policy_id": ["POL-1001", "POL-1002"],
        "customer_name": ["John", "Sarah"],
        "carrier": ["ABC", "ABC"],
        "premium": [1200, 1500],
        "status": ["Active", "Active"],
        "effective_date": ["2025-01-01", "2025-01-01"],
        "expiration_date": ["2026-01-01", "2026-01-01"],
    })

    # Create sample Agency B data with one premium discrepancy
    agency_b = pd.DataFrame({
        "policy_id": ["POL-1001", "POL-1002"],
        "customer_name": ["John", "Sarah"],
        "carrier": ["ABC", "ABC"],
        "premium": [1200, 2000],
        "status": ["Active", "Active"],
        "effective_date": ["2025-01-01", "2025-01-01"],
        "expiration_date": ["2026-01-01", "2026-01-01"],
    })

    # Save sample files
    agency_a.to_parquet(agency_a_dir / "sample.parquet", index=False)
    agency_b.to_parquet(agency_b_dir / "sample.parquet", index=False)

    # Run the function from the temporary directory
    monkeypatch.chdir(tmp_path)

    result = run_reconciliation()

    # Verify one exception was identified
    assert len(result) == 1
    assert result.iloc[0]["policy_id"] == "POL-1002"
    assert result.iloc[0]["discrepancy_types"] == ["premium"]

    # Verify output files were created
    assert (tmp_path / "data" / "exceptions" / "reconciliation_exceptions.csv").exists()
    assert (tmp_path / "data" / "exceptions" / "reconciliation_exceptions.parquet").exists()
