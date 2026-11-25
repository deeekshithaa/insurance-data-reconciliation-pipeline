import pandas as pd
from pathlib import Path
from datetime import datetime, timezone
import ast


def parse_discrepancy_types(value):
    """Convert discrepancy types into a usable Python list."""
    if isinstance(value, list):
        return value

    if pd.isna(value):
        return []

    if isinstance(value, str):
        try:
            parsed = ast.literal_eval(value)
            return parsed if isinstance(parsed, list) else [str(parsed)]
        except (ValueError, SyntaxError):
            return [value]

    return []


def assign_priority(discrepancies):
    """Assign review priority based on discrepancy severity."""
    discrepancies = [str(item).lower() for item in discrepancies]

    if "premium" in discrepancies or len(discrepancies) >= 2:
        return "High"

    if discrepancies:
        return "Medium"

    return "Low"


def build_exception_management_dataset(df):
    """Enrich reconciliation exceptions with review workflow fields."""

    exceptions = df.copy()

    exceptions["discrepancy_types"] = exceptions[
        "discrepancy_types"
    ].apply(parse_discrepancy_types)

    exceptions["exception_id"] = (
        "EXC-" + exceptions["policy_id"].astype(str)
    )

    exceptions["priority"] = exceptions["discrepancy_types"].apply(
        assign_priority
    )

    exceptions["review_status"] = "Open"
    exceptions["assigned_reviewer"] = None
    exceptions["resolution_notes"] = None
    exceptions["resolved_at"] = None

    exceptions["created_at"] = datetime.now(timezone.utc).isoformat()

    return exceptions


def save_exception_management_dataset(
    exceptions,
    output_path="data/exceptions/exception_management.csv"
):
    """Save the enriched exception dataset."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    exceptions.to_csv(output_path, index=False)

    return output_path

def update_exception_status(
    exception_id,
    new_status,
    reviewer,
    resolution_notes,
    file_path="data/exceptions/exception_management.csv"
):
    """Update the status and review details of a specific exception."""

    allowed_statuses = ["Open", "In Review", "Resolved"]

    if new_status not in allowed_statuses:
        raise ValueError(
            f"Status must be one of {allowed_statuses}"
        )

    file_path = Path(file_path)

    exceptions = pd.read_csv(file_path)

    # Ensure workflow fields can hold text values
    for column in ["review_status", "assigned_reviewer", "resolution_notes", "resolved_at"]:
        exceptions[column] = exceptions[column].astype("string")

    matching_rows = exceptions[
        exceptions["exception_id"] == exception_id
    ]

    if matching_rows.empty:
        raise ValueError(f"Exception not found: {exception_id}")

    exceptions.loc[
        exceptions["exception_id"] == exception_id,
        "review_status"
    ] = new_status

    exceptions.loc[
        exceptions["exception_id"] == exception_id,
        "assigned_reviewer"
    ] = reviewer

    exceptions.loc[
        exceptions["exception_id"] == exception_id,
        "resolution_notes"
    ] = resolution_notes

    if new_status == "Resolved":
        exceptions.loc[
            exceptions["exception_id"] == exception_id,
            "resolved_at"
        ] = datetime.now(timezone.utc).isoformat()

    exceptions.to_csv(file_path, index=False)

    return exceptions.loc[
        exceptions["exception_id"] == exception_id
    ]