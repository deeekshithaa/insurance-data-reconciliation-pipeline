import pandas as pd

from src.exceptions.exception_manager import (
    build_exception_management_dataset,
    save_exception_management_dataset,
)


def main():
    input_path = "data/exceptions/reconciliation_exceptions.csv"

    reconciliation_df = pd.read_csv(input_path)

    managed_exceptions = build_exception_management_dataset(
        reconciliation_df
    )

    output_path = save_exception_management_dataset(
        managed_exceptions
    )

    print(f"Exception management dataset created: {output_path}")
    print(f"Total exceptions: {len(managed_exceptions)}")

    print("\nPriority breakdown:")
    print(managed_exceptions["priority"].value_counts())

    print("\nReview status breakdown:")
    print(managed_exceptions["review_status"].value_counts())


if __name__ == "__main__":
    main()