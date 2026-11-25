import pandas as pd

from src.reconciliation.reconciliation_engine import (
    prepare_for_reconciliation,
    match_agencies,
    compare_matched_records,
    classify_discrepancies,
)


def build_fact_policy(agency_a, agency_b):
    """Build a policy-level analytical fact dataset."""

    # Step 1: Remove duplicates and isolate conflicting records
    agency_a_clean, agency_a_conflicts = prepare_for_reconciliation(
        agency_a
    )

    agency_b_clean, agency_b_conflicts = prepare_for_reconciliation(
        agency_b
    )

    # Step 2: Full outer join both agencies
    reconciled = match_agencies(
        agency_a_clean,
        agency_b_clean,
    )

    # Step 3: Compare matched records
    compared = compare_matched_records(reconciled)

    # Step 4: Classify discrepancies
    exceptions = classify_discrepancies(compared)

    # Step 5: Attach discrepancy information to the full dataset
    fact = reconciled.copy()

    fact["match_status"] = fact["_merge"].map({
        "both": "Matched",
        "left_only": "Missing from Agency B",
        "right_only": "Missing from Agency A",
    })

    discrepancy_columns = [
        "policy_id",
        "has_discrepancy",
        "discrepancy_types",
    ]

    fact = fact.merge(
        exceptions[discrepancy_columns],
        on="policy_id",
        how="left",
    )

    # Step 6: Fill values for policies without field discrepancies
    fact["has_discrepancy"] = (
        fact["has_discrepancy"].fillna(False).astype(bool)
    )

    fact["discrepancy_types"] = fact["discrepancy_types"].apply(
        lambda value: value if isinstance(value, list) else []
    )

    # Step 7: Calculate premium difference for matched policies
    fact["premium_difference"] = (
        fact["premium_b"] - fact["premium_a"]
    )

    # Step 8: Add useful analytical flags
    fact["premium_mismatch"] = (
        fact["premium_a"].notna()
        & fact["premium_b"].notna()
        & fact["premium_a"].ne(fact["premium_b"])
    )

    fact["customer_name_mismatch"] = (
        (fact["match_status"] == "Matched")
        & (
            (
                fact["customer_name_a"].notna()
                & fact["customer_name_b"].notna()
                & fact["customer_name_a"].ne(fact["customer_name_b"])
            )
            |
            (
                fact["customer_name_a"].isna()
                != fact["customer_name_b"].isna()
            )
        )
    )

    # Step 9: Remove technical merge column
    fact = fact.drop(columns=["_merge"])

    # Step 10: Return the analytical dataset
    return fact