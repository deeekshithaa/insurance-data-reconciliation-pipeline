import pandas as pd


def prepare_for_reconciliation(df):
    """
    Prepare a dataset for reconciliation.

    1. Remove exact duplicate rows.
    2. Identify policy IDs with conflicting records.
    3. Exclude conflicting policy IDs from the clean dataset.

    Returns:
        clean_df: Dataset ready for reconciliation.
        conflict_df: Records that require investigation.
    """

    df = df.copy()

    # Step 1: Remove exact duplicate rows
    df = df.drop_duplicates()

    # Step 2: Identify policy IDs with conflicting records
    duplicate_policy_mask = df["policy_id"].duplicated(keep=False)

    conflict_df = df[duplicate_policy_mask].copy()

    # Step 3: Exclude conflicting policy IDs from clean data
    clean_df = df[~duplicate_policy_mask].copy()

    return clean_df, conflict_df

def match_agencies(agency_a_df, agency_b_df):
    """
    Match policies between Agency A and Agency B
    using a full outer join on policy_id.
    """

    matched_df = agency_a_df.merge(
        agency_b_df,
        on="policy_id",
        how="outer",
        suffixes=("_a", "_b"),
        indicator=True,
    )

    return matched_df

def compare_matched_records(reconciled_df):
    """
    Compare fields for policies that exist in both agencies.
    """

    # Keep only policies matched in both agencies
    matched_df = reconciled_df[
        reconciled_df["_merge"] == "both"
    ].copy()

    # Fields we want to compare
    fields_to_compare = [
        "customer_name",
        "carrier",
        "premium",
        "status",
        "effective_date",
        "expiration_date",
    ]

    # Compare each field between Agency A and Agency B
    for field in fields_to_compare:

        column_a = f"{field}_a"
        column_b = f"{field}_b"

        matched_df[f"{field}_match"] = (
            matched_df[column_a].eq(matched_df[column_b])
            | (
                matched_df[column_a].isna()
                & matched_df[column_b].isna()
            )
        )

    return matched_df

def classify_discrepancies(compared_df):
    """
    Identify policies with discrepancies and classify the issue types.
    """

    compared_df = compared_df.copy()

    fields_to_compare = [
        "customer_name",
        "carrier",
        "premium",
        "status",
        "effective_date",
        "expiration_date",
    ]

    match_columns = [
        f"{field}_match" for field in fields_to_compare
    ]

    # Identify policies with at least one mismatch
    compared_df["has_discrepancy"] = (
        ~compared_df[match_columns].all(axis=1)
    )

    # Identify the fields that don't match for each policy
    compared_df["discrepancy_types"] = compared_df.apply(
        lambda row: [
            field
            for field in fields_to_compare
            if not row[f"{field}_match"]
        ],
        axis=1,
    )

    # Keep only policies with discrepancies
    exceptions_df = compared_df[
        compared_df["has_discrepancy"]
    ].copy()

    return exceptions_df

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