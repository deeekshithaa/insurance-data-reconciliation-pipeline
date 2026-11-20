import pandas as pd


REQUIRED_COLUMNS = [
    "policy_id",
    "customer_name",
    "premium",
    "status",
]


def check_required_columns(df):
    """
    Check whether all required columns exist.
    """

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    return missing_columns


def check_missing_policy_ids(df):
    """
    Count records with missing policy IDs.
    """

    return df["policy_id"].isna().sum()


def check_duplicate_policy_ids(df):
    """
    Count records with repeated policy IDs.
    """

    return df["policy_id"].duplicated().sum()


def check_missing_customer_names(df):
    """
    Count records with missing customer names.
    """

    return df["customer_name"].isna().sum()


def check_missing_premiums(df):
    """
    Count records with missing premium values.
    """

    return df["premium"].isna().sum()


def generate_quality_report(df):
    """
    Generate a basic data quality report.
    """

    missing_columns = check_required_columns(df)

    if missing_columns:
        return {
            "quality_status": "FAILED",
            "missing_required_columns": missing_columns,
        }

    report = {
        "total_records": int(len(df)),
        "missing_policy_ids": int(check_missing_policy_ids(df)),
        "duplicate_policy_ids": int(check_duplicate_policy_ids(df)),
        "missing_customer_names": int(check_missing_customer_names(df)),
        "missing_premiums": int(check_missing_premiums(df)),
    }

    issue_count = (
        report["missing_policy_ids"]
        + report["duplicate_policy_ids"]
        + report["missing_customer_names"]
        + report["missing_premiums"]
    )

    report["quality_status"] = "PASS" if issue_count == 0 else "WARNING"

    return report