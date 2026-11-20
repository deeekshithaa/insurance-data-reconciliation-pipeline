import pandas as pd

from src.transformations.silver_pipeline import transform_dataframe


def test_transform_dataframe_standardizes_policy_ids():
    df = pd.DataFrame({
        "policy_id": ["POL1001", "POL-1002"],
        "status": ["In Force", "Active"],
    })

    result = transform_dataframe(df)

    assert result["policy_id"].tolist() == ["POL-1001", "POL-1002"]


def test_transform_dataframe_normalizes_statuses():
    df = pd.DataFrame({
        "policy_id": ["POL1001", "POL1002", "POL1003"],
        "status": ["In Force", "Expired", "Pending"],
    })

    result = transform_dataframe(df)

    assert result["status"].tolist() == ["Active", "Terminated", "Pending"]


def test_transform_dataframe_preserves_original_dataframe():
    df = pd.DataFrame({
        "policy_id": ["POL1001"],
        "status": ["In Force"],
    })

    original = df.copy(deep=True)

    transform_dataframe(df)

    pd.testing.assert_frame_equal(df, original)


def test_transform_dataframe_preserves_other_columns():
    df = pd.DataFrame({
        "policy_id": ["POL1001"],
        "status": ["In Force"],
        "customer_name": ["John Smith"],
        "premium": [9897.84],
    })

    result = transform_dataframe(df)

    assert result["customer_name"].tolist() == ["John Smith"]
    assert result["premium"].tolist() == [9897.84]