import pandas as pd
from pathlib import Path

from src.reporting.exception_report import generate_exception_summary


def main():
    input_path = "data/exceptions/exception_management.csv"
    output_path = "data/exceptions/exception_summary.csv"

    exceptions_df = pd.read_csv(input_path)

    summary = generate_exception_summary(exceptions_df)

    print("\n========== EXCEPTION REPORT ==========\n")

    for metric, value in summary.items():
        formatted_metric = metric.replace("_", " ").title()
        print(f"{formatted_metric}: {value}")

    summary_df = pd.DataFrame([summary])

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    summary_df.to_csv(output_file, index=False)

    print(f"\nReport saved to: {output_file}")

    print("\n====================================\n")


if __name__ == "__main__":
    main()