from pathlib import Path
import pandas as pd

from src.reconciliation.reconciliation_engine import (
    prepare_for_reconciliation,
    match_agencies,
    compare_matched_records,
    classify_discrepancies,
)


def run_reconciliation():
    # Step 1: Read Silver data
    agency_a = pd.read_parquet("data/silver/agency_a")
    agency_b = pd.read_parquet("data/silver/agency_b")

    # Step 2: Prepare datasets
    agency_a_clean, agency_a_conflicts = prepare_for_reconciliation(agency_a)
    agency_b_clean, agency_b_conflicts = prepare_for_reconciliation(agency_b)

    # Step 3: Match policies
    reconciled_df = match_agencies(
        agency_a_clean,
        agency_b_clean,
    )

    # Step 4: Compare fields
    compared_df = compare_matched_records(reconciled_df)

    # Step 5: Classify exceptions
    exceptions_df = classify_discrepancies(compared_df)

    # Step 6: Create output directory
    output_dir = Path("data/exceptions")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 7: Save exceptions
    csv_file = output_dir / "reconciliation_exceptions.csv"
    parquet_file = output_dir / "reconciliation_exceptions.parquet"

    exceptions_df.to_csv(csv_file, index=False)
    exceptions_df.to_parquet(parquet_file, index=False, engine="pyarrow")

    # Step 8: Print summary
    print("RECONCILIATION COMPLETE")
    print("=" * 40)
    print("Matched policies:", len(compared_df))
    print("Total exceptions:", len(exceptions_df))
    print("Agency A conflicts:", len(agency_a_conflicts))
    print("Agency B conflicts:", len(agency_b_conflicts))

    print("\nDiscrepancy summary:")
    print(exceptions_df["discrepancy_types"].explode().value_counts())

    print("\nFiles saved:")
    print(csv_file)
    print(parquet_file)

    return exceptions_df


if __name__ == "__main__":
    run_reconciliation()