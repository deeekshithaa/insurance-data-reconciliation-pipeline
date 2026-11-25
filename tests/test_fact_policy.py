import pandas as pd

from src.marts.fact_policy import build_fact_policy


def test_fact_policy_counts_and_mismatch_flags():
    agency_a = pd.DataFrame([
        {
            "policy_id": "POL-1001",
            "customer_name": "John Smith",
            "carrier": "ABC Insurance",
            "premium": 1000.0,
            "status": "Active",
            "effective_date": "2025-01-01",
            "expiration_date": "2026-01-01",
        },
        {
            "policy_id": "POL-1002",
            "customer_name": "Jane Doe",
            "carrier": "ABC Insurance",
            "premium": 2000.0,
            "status": "Active",
            "effective_date": "2025-01-01",
            "expiration_date": "2026-01-01",
        },
    ])

    agency_b = pd.DataFrame([
        {
            "policy_id": "POL-1001",
            "customer_name": "John Smith",
            "carrier": "ABC Insurance",
            "premium": 1500.0,
            "status": "Active",
            "effective_date": "2025-01-01",
            "expiration_date": "2026-01-01",
        },
        {
            "policy_id": "POL-1002",
            "customer_name": None,
            "carrier": "ABC Insurance",
            "premium": 2000.0,
            "status": "Active",
            "effective_date": "2025-01-01",
            "expiration_date": "2026-01-01",
        },
        {
            "policy_id": "POL-1003",
            "customer_name": "New Customer",
            "carrier": "ABC Insurance",
            "premium": 3000.0,
            "status": "Active",
            "effective_date": "2025-01-01",
            "expiration_date": "2026-01-01",
        },
    ])

    fact = build_fact_policy(agency_a, agency_b)

    assert len(fact) == 3
    assert (fact["match_status"] == "Matched").sum() == 2
    assert (fact["match_status"] == "Missing from Agency A").sum() == 1

    assert fact["premium_mismatch"].sum() == 1
    assert fact["customer_name_mismatch"].sum() == 1