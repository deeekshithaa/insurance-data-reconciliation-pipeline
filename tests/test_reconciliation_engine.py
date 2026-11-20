import pandas as pd

from src.reconciliation.reconciliation_engine import (
    prepare_for_reconciliation,
    match_agencies,
    compare_matched_records,
    classify_discrepancies,
)


def test_prepare_for_reconciliation():
    df = pd.DataFrame({
        "policy_id": ["POL-1001", "POL-1001", "POL-1002", "POL-1003"],
        "customer_name": ["John", "John", "Sarah", "Mike"],
        "premium": [1200, 1200, 1500, 1800],
    })

    clean_df, conflict_df = prepare_for_reconciliation(df)

    assert len(clean_df) == 3
    assert len(conflict_df) == 0
    assert clean_df["policy_id"].tolist() == [
        "POL-1001", "POL-1002", "POL-1003"
    ]


def test_match_agencies():
    agency_a = pd.DataFrame({
        "policy_id": ["POL-1001", "POL-1002"],
        "premium": [1200, 1500],
    })

    agency_b = pd.DataFrame({
        "policy_id": ["POL-1001", "POL-1003"],
        "premium": [1200, 1800],
    })

    result = match_agencies(agency_a, agency_b)

    assert len(result) == 3
    assert result["_merge"].value_counts().to_dict() == {
        "both": 1,
        "left_only": 1,
        "right_only": 1,
    }


def test_compare_matched_records():
    df = pd.DataFrame({
        "policy_id": ["POL-1001", "POL-1002", "POL-1003"],
        "customer_name_a": ["John", "Sarah", None],
        "customer_name_b": ["John", "Sarah", None],
        "carrier_a": ["ABC", "ABC", "ABC"],
        "carrier_b": ["ABC", "ABC", "ABC"],
        "premium_a": [1200, 1500, 1800],
        "premium_b": [1200, 2000, 1800],
        "status_a": ["Active", "Active", "Active"],
        "status_b": ["Active", "Active", "Active"],
        "effective_date_a": ["2025-01-01"] * 3,
        "effective_date_b": ["2025-01-01"] * 3,
        "expiration_date_a": ["2026-01-01"] * 3,
        "expiration_date_b": ["2026-01-01"] * 3,
        "_merge": ["both", "both", "left_only"],
    })

    result = compare_matched_records(df)

    assert len(result) == 2

    assert result.iloc[0]["premium_match"] == True
    assert result.iloc[1]["premium_match"] == False

    assert result.iloc[0]["customer_name_match"] == True
    assert result.iloc[1]["customer_name_match"] == True


def test_classify_discrepancies():
    df = pd.DataFrame({
        "policy_id": ["POL-1001", "POL-1002", "POL-1003"],
        "customer_name_match": [True, False, True],
        "carrier_match": [True, True, True],
        "premium_match": [False, True, True],
        "status_match": [True, True, True],
        "effective_date_match": [True, True, True],
        "expiration_date_match": [True, True, True],
    })

    result = classify_discrepancies(df)

    assert len(result) == 2

    assert result["policy_id"].tolist() == [
        "POL-1001",
        "POL-1002",
    ]

    assert result["discrepancy_types"].tolist() == [
        ["premium"],
        ["customer_name"],
    ]

    assert result["has_discrepancy"].all()