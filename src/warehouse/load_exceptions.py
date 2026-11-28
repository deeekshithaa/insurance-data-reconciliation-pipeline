import pandas as pd

from connection import get_engine


def load_exceptions():
    """Load the exception management dataset into PostgreSQL."""

    source_file = "data/exceptions/exception_management.csv"
    table_name = "exception_management"

    df = pd.read_csv(source_file)

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
    load_exceptions()