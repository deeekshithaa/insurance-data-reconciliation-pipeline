from pathlib import Path
import pandas as pd

from src.reconciliation.reconciliation_engine import (
    prepare_for_reconciliation,
    match_agencies,
    compare_matched_records,
    classify_discrepancies,
)


def run_reconciliation():
    agency_a = pd.read_parquet("data/silver/agency_a")
    agency_b = pd.read_parquet("data/silver/agency_b")

    agency_a_clean, agency_a_conflicts = prepare_for_reconciliation(agency_a)
    agency_b_clean, agency_b_conflicts = prepare_for_reconciliation(agency_b)

    reconciled_df = match_agencies(agency_a_clean, agency_b_clean)

    unmatched_df = reconciled_df[
        reconciled_df["_merge"] != "both"
    ].copy()

    unmatched_df["exception_type"] = unmatched_df["_merge"].map(
        {
            "left_only": "Missing from Agency B",
            "right_only": "Missing from Agency A",
        }
    )

    compared_df = compare_matched_records(reconciled_df)
    exceptions_df = classify_discrepancies(compared_df)

    output_dir = Path("data/exceptions")
    output_dir.mkdir(parents=True, exist_ok=True)

    exceptions_df.to_csv(
        output_dir / "reconciliation_exceptions.csv",
        index=False,
    )

    exceptions_df.to_parquet(
        output_dir / "reconciliation_exceptions.parquet",
        index=False,
        engine="pyarrow",
    )

    unmatched_df.to_csv(
        output_dir / "unmatched_policies.csv",
        index=False,
    )

    unmatched_df.to_parquet(
        output_dir / "unmatched_policies.parquet",
        index=False,
        engine="pyarrow",
    )

    print("RECONCILIATION COMPLETE")
    print("=" * 40)
    print("Matched policies:", len(compared_df))
    print("Field-level exceptions:", len(exceptions_df))
    print("Unmatched policies:", len(unmatched_df))
    print("Agency A conflicts:", len(agency_a_conflicts))
    print("Agency B conflicts:", len(agency_b_conflicts))

    print("\nField discrepancy summary:")
    print(exceptions_df["discrepancy_types"].explode().value_counts())

    print("\nUnmatched policy summary:")
    print(unmatched_df["exception_type"].value_counts())

    print("\nFiles saved:")
    print(output_dir / "reconciliation_exceptions.csv")
    print(output_dir / "reconciliation_exceptions.parquet")
    print(output_dir / "unmatched_policies.csv")
    print(output_dir / "unmatched_policies.parquet")

    return exceptions_df, unmatched_df


if __name__ == "__main__":
    run_reconciliation()