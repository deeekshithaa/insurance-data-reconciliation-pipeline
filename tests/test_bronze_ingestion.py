
import pandas as pd
import pytest

from src.ingestion import bronze_ingestion


def create_sample_csv(path):
    """Create a small CSV with two identical policy records."""

    sample = pd.DataFrame({
        "policy_id": ["POL-1001", "POL-1001"],
        "customer_name": ["John Smith", "John Smith"],
        "carrier": ["Global Insurance", "Global Insurance"],
        "premium": [9897.84, 9897.84],
        "status": ["Active", "Active"],
        "effective_date": ["2026-02-27", "2026-02-27"],
        "expiration_date": ["2027-02-27", "2027-02-27"],
    })

    sample.to_csv(path, index=False)


def test_successful_bronze_ingestion(tmp_path, monkeypatch):
    source_file = tmp_path / "agency_a.csv"
    bronze_dir = tmp_path / "bronze"

    create_sample_csv(source_file)

    monkeypatch.setattr(
        bronze_ingestion,
        "BRONZE_DIR",
        bronze_dir,
    )

    result = bronze_ingestion.ingest_csv_to_bronze(
        "agency_a",
        source_file,
    )

    df = pd.read_parquet(result["output_file"])

    assert result["status"] == "ingested"
    assert len(df) == 2
    assert len(df.columns) == 11
    assert df["source_system"].iloc[0] == "agency_a"
    assert df["source_file"].iloc[0] == "agency_a.csv"
    assert df["ingestion_batch_id"].notna().all()
    assert df.duplicated().sum() == 1


def test_duplicate_ingestion_is_skipped(tmp_path, monkeypatch):
    source_file = tmp_path / "agency_a.csv"
    bronze_dir = tmp_path / "bronze"

    create_sample_csv(source_file)

    monkeypatch.setattr(
        bronze_ingestion,
        "BRONZE_DIR",
        bronze_dir,
    )

    first_result = bronze_ingestion.ingest_csv_to_bronze(
        "agency_a",
        source_file,
    )

    second_result = bronze_ingestion.ingest_csv_to_bronze(
        "agency_a",
        source_file,
    )

    assert first_result["status"] == "ingested"
    assert second_result["status"] == "skipped"
    assert first_result["batch_id"] == second_result["batch_id"]


def test_changed_source_creates_new_batch(tmp_path, monkeypatch):
    source_file = tmp_path / "agency_a.csv"
    bronze_dir = tmp_path / "bronze"

    create_sample_csv(source_file)

    monkeypatch.setattr(
        bronze_ingestion,
        "BRONZE_DIR",
        bronze_dir,
    )

    first_result = bronze_ingestion.ingest_csv_to_bronze(
        "agency_a",
        source_file,
    )

    # Change the source file contents.
    df = pd.read_csv(source_file)
    df.loc[0, "premium"] = 12000.00
    df.to_csv(source_file, index=False)

    second_result = bronze_ingestion.ingest_csv_to_bronze(
        "agency_a",
        source_file,
    )

    assert second_result["status"] == "ingested"
    assert first_result["batch_id"] != second_result["batch_id"]
