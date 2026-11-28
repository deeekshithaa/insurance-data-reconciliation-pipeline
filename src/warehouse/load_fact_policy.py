import pandas as pd
import numpy as np

from connection import get_engine


def load_fact_policy():
    """Load the Fact Policy dataset into PostgreSQL."""

    source_file = "data/processed/fact_policy.parquet"
    table_name = "fact_policy"

    df = pd.read_parquet(source_file)

    # Convert NumPy arrays into PostgreSQL-compatible strings
    df["discrepancy_types"] = df["discrepancy_types"].apply(
        lambda x: ", ".join(x.tolist())
        if isinstance(x, np.ndarray)
        else ", ".join(x)
        if isinstance(x, list)
        else str(x)
        if pd.notna(x)
        else ""
    )

    engine = get_engine()

    try:
        df.to_sql(
            name=table_name,
            con=engine,
            schema="public",
            if_exists="replace",
            index=False,
            chunksize=100,
        )

        print(f"Successfully loaded {len(df)} records into {table_name}.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    load_fact_policy()