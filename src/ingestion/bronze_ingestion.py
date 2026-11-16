
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_FILES = {
    "agency_a": PROJECT_ROOT / "data/raw/agency_a/agency_a_policies.csv",
    "agency_b": PROJECT_ROOT / "data/raw/agency_b/agency_b_policies.csv",
}

BRONZE_DIR = PROJECT_ROOT / "data/bronze"

REQUIRED_COLUMNS = {
    "policy_id",
    "customer_name",
    "carrier",
    "premium",
    "status",
    "effective_date",
    "expiration_date",
}


def calculate_file_hash(file_path: Path) -> str:
    """Calculate a SHA-256 hash of the source file."""
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def ingest_csv_to_bronze(
    source_system: str,
    source_file: Path,
) -> dict:
    """Ingest one source CSV into the Bronze layer."""

    if not source_file.exists():
        raise FileNotFoundError(
            f"Source file not found: {source_file}"
        )

    if source_system not in {"agency_a", "agency_b"}:
        raise ValueError(f"Unsupported source system: {source_system}")

    # Identify this exact version of the source file.
    file_hash = calculate_file_hash(source_file)
    batch_id = f"{source_system}_{file_hash[:16]}"

    output_dir = BRONZE_DIR / source_system
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{batch_id}.parquet"

    # Prevent duplicate ingestion of unchanged source files.
    if output_file.exists():
        print(f"SKIPPED: {source_system} already ingested.")
        return {
            "source_system": source_system,
            "batch_id": batch_id,
            "status": "skipped",
            "output_file": str(output_file),
        }

    # Read the source data without changing its business columns.
    df = pd.read_csv(source_file)

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"{source_system} is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    # Add ingestion metadata.
    df["source_system"] = source_system
    df["source_file"] = source_file.name
    df["ingestion_timestamp"] = datetime.now(
        timezone.utc
    ).isoformat()
    df["ingestion_batch_id"] = batch_id

    # Write the Bronze dataset as Parquet.
    df.to_parquet(
        output_file,
        engine="pyarrow",
        index=False,
    )

    print(
        f"INGESTED: {source_system} | "
        f"Rows: {len(df)} | "
        f"Batch: {batch_id}"
    )

    return {
        "source_system": source_system,
        "batch_id": batch_id,
        "status": "ingested",
        "row_count": len(df),
        "output_file": str(output_file),
    }


def main():
    """Run Bronze ingestion for both agencies."""

    results = []

    for source_system, source_file in SOURCE_FILES.items():
        result = ingest_csv_to_bronze(
            source_system=source_system,
            source_file=source_file,
        )
        results.append(result)

    print("\nBronze ingestion summary:")

    for result in results:
        print(result)


if __name__ == "__main__":
    main()
