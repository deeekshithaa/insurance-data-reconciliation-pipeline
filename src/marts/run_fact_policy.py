from pathlib import Path
import pandas as pd

from src.marts.fact_policy import build_fact_policy


def main():
    # Read Silver datasets
    agency_a = pd.read_parquet("data/silver/agency_a")
    agency_b = pd.read_parquet("data/silver/agency_b")

    # Build Fact dataset
    fact_policy = build_fact_policy(agency_a, agency_b)

    # Save outputs
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "fact_policy.csv"
    parquet_path = output_dir / "fact_policy.parquet"

    fact_policy.to_csv(csv_path, index=False)
    fact_policy.to_parquet(parquet_path, index=False)

    # Print pipeline summary
    print("\nFACT POLICY DATASET CREATED")
    print("=" * 40)

    print("Total policies:", len(fact_policy))
    print("Matched:", (fact_policy["match_status"] == "Matched").sum())
    print("Missing from Agency A:", (fact_policy["match_status"] == "Missing from Agency A").sum())
    print("Missing from Agency B:", (fact_policy["match_status"] == "Missing from Agency B").sum())
    print("Field discrepancies:", fact_policy["has_discrepancy"].sum())
    print("Premium mismatches:", fact_policy["premium_mismatch"].sum())
    print("Customer name mismatches:", fact_policy["customer_name_mismatch"].sum())

    print("\nFiles saved:")
    print(csv_path)
    print(parquet_path)


if __name__ == "__main__":
    main()