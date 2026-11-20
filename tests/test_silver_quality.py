import pandas as pd

from src.quality.silver_quality import (
    check_required_columns,
    check_missing_policy_ids,
    check_duplicate_policy_ids,
    check_missing_customer_names,
    check_missing_premiums,
    generate_quality_report,
)


def create_sample_dataframe():
    return pd.DataFrame({
        "policy_id": ["POL-1001", "POL-1002", "POL-1001", None],
        "customer_name": ["John Smith", "Jane Doe", None, "David Lee"],
        "premium": [1000.00, 2000.00, 1500.00, None],
        "status": ["Active", "Pending", "Active", "Terminated"],
    })


def test_required_columns_exist():
    df = create_sample_dataframe()

    result = check_required_columns(df)

    assert result == []


def test_missing_required_column():
    df = create_sample_dataframe().drop(columns=["premium"])

    result = check_required_columns(df)

    assert result == ["premium"]


def test_missing_policy_ids():
    df = create_sample_dataframe()

    result = check_missing_policy_ids(df)

    assert result == 1


def test_duplicate_policy_ids():
    df = create_sample_dataframe()

    result = check_duplicate_policy_ids(df)

    assert result == 1


def test_missing_customer_names():
    df = create_sample_dataframe()

    result = check_missing_customer_names(df)

    assert result == 1


def test_missing_premiums():
    df = create_sample_dataframe()

    result = check_missing_premiums(df)

    assert result == 1


def test_generate_quality_report():
    df = create_sample_dataframe()

    result = generate_quality_report(df)

    assert result == {
        "total_records": 4,
        "missing_policy_ids": 1,
        "duplicate_policy_ids": 1,
        "missing_customer_names": 1,
        "missing_premiums": 1,
        "quality_status": "WARNING",
    }


    df = create_sample_dataframe().drop(columns=["premium"])

    result = generate_quality_report(df)

    assert result == {
    "quality_status": "FAILED",
    "missing_required_columns": ["premium"],
}