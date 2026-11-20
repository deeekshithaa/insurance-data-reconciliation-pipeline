from pathlib import Path
import pandas as pd

from src.transformations.silver_transformations import (
    standardize_policy_id,
    normalize_status,
)


def transform_dataframe(df):
    """
    Apply Silver transformations to a DataFrame.
    """

    df = df.copy()

    df["policy_id"] = df["policy_id"].apply(standardize_policy_id)
    df["status"] = df["status"].apply(normalize_status)

    return df


def process_bronze_file(bronze_file, source_system):
    """
    Read a Bronze Parquet file, transform it,
    and save the result to the Silver layer.
    """

    bronze_file = Path(bronze_file)

    df = pd.read_parquet(bronze_file)

    silver_df = transform_dataframe(df)

    output_dir = Path("data/silver") / source_system
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / bronze_file.name

    silver_df.to_parquet(output_file, index=False, engine="pyarrow")

    print(f"Silver data saved: {output_file}")
    print(f"Rows processed: {len(silver_df)}")

    return silver_df


def main():
    sources = {
        "agency_a": "data/bronze/agency_a",
        "agency_b": "data/bronze/agency_b",
    }

    for source_system, directory in sources.items():
        bronze_files = list(Path(directory).glob("*.parquet"))

        for bronze_file in bronze_files:
            process_bronze_file(bronze_file, source_system)


if __name__ == "__main__":
    main()