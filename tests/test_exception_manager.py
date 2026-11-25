import pandas as pd

from src.exceptions.exception_manager import (
    build_exception_management_dataset,
)


def test_build_exception_management_dataset():
    sample_data = pd.DataFrame([
        {
            "policy_id": "POL-1001",
            "discrepancy_types": "['premium']",
        },
        {
            "policy_id": "POL-1002",
            "discrepancy_types": "['customer_name']",
        },
        {
            "policy_id": "POL-1003",
            "discrepancy_types": "['premium', 'customer_name']",
        },
    ])

    result = build_exception_management_dataset(sample_data)

    assert len(result) == 3
    assert result["exception_id"].tolist() == [
        "EXC-POL-1001",
        "EXC-POL-1002",
        "EXC-POL-1003",
    ]

    assert result["priority"].tolist() == [
        "High",
        "Medium",
        "High",
    ]

    assert result["review_status"].tolist() == [
        "Open",
        "Open",
        "Open",
    ]

    assert result["assigned_reviewer"].isna().all()
    assert result["resolution_notes"].isna().all()