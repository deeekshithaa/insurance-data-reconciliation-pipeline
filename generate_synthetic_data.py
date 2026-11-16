
import json
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


# 1. CONFIGURATION

RANDOM_SEED = 42

BASE_POLICY_COUNT = 1000

PREMIUM_MISMATCH_COUNT = 100
DUPLICATE_COUNT = 50
MISSING_CUSTOMER_COUNT = 30
UNMATCHED_POLICY_COUNT = 50



# 2. PROJECT PATHS

PROJECT_ROOT = Path(__file__).resolve().parent

AGENCY_A_PATH = (
    PROJECT_ROOT / "data/raw/agency_a/agency_a_policies.csv"
)

AGENCY_B_PATH = (
    PROJECT_ROOT / "data/raw/agency_b/agency_b_policies.csv"
)

METADATA_PATH = (
    PROJECT_ROOT / "data/raw/generation_metadata.json"
)


# 3. GENERATE BASE POLICIES

def generate_base_policies(rng):
    """Generate the original shared insurance policies."""

    customers = [
        "John Smith",
        "Sarah Johnson",
        "Michael Brown",
        "Emily Davis",
        "David Wilson",
        "Olivia Martin",
        "James Anderson",
        "Sophia Taylor",
        "Daniel Thomas",
        "Emma Garcia",
    ]

    carriers = [
        "ABC Insurance",
        "XYZ Insurance",
        "Global Insurance",
        "National Insurance",
    ]

    statuses = ["Active", "Expired", "Pending"]

    records = []

    for i in range(BASE_POLICY_COUNT):

        policy_number = 1001 + i

        effective_date = date(2026, 1, 1) + timedelta(
            days=rng.randint(0, 300)
        )

        expiration_date = effective_date + timedelta(days=365)

        record = {
            "policy_id": f"POL-{policy_number}",
            "customer_name": rng.choice(customers),
            "carrier": rng.choice(carriers),
            "premium": round(rng.uniform(5000, 25000), 2),
            "status": rng.choice(statuses),
            "effective_date": effective_date.isoformat(),
            "expiration_date": expiration_date.isoformat(),
        }

        records.append(record)

    return pd.DataFrame(records)


# 4. CREATE AGENCY A

def create_agency_a(base_policies):
    """Create Agency A's original source dataset."""

    return base_policies.copy(deep=True)


# 5. CREATE AGENCY B

def create_agency_b(base_policies, rng):
    """Create Agency B data with controlled discrepancies."""

    agency_b = base_policies.copy(deep=True)

    # Track deliberately injected scenarios.
    metadata = {
        "premium_mismatch_policy_ids": [],
        "duplicate_policy_ids": [],
        "missing_customer_policy_ids": [],
        "unmatched_policy_ids": [],
    }

    # A. Change policy ID formatting

    agency_b["policy_id"] = agency_b["policy_id"].str.replace(
        "-", "", regex=False
    )

    # B. Introduce premium mismatches

    mismatch_indices = rng.sample(
        list(agency_b.index),
        PREMIUM_MISMATCH_COUNT,
    )

    for index in mismatch_indices:
        agency_b.loc[index, "premium"] = round(
            agency_b.loc[index, "premium"] + 500,
            2,
        )

        metadata["premium_mismatch_policy_ids"].append(
            agency_b.loc[index, "policy_id"]
        )


    # C. Introduce missing customer names

    missing_indices = rng.sample(
        list(agency_b.index),
        MISSING_CUSTOMER_COUNT,
    )

    for index in missing_indices:
        agency_b.loc[index, "customer_name"] = None

        metadata["missing_customer_policy_ids"].append(
            agency_b.loc[index, "policy_id"]
        )

    # D. Introduce duplicate records

    duplicate_indices = rng.sample(
        list(agency_b.index),
        DUPLICATE_COUNT,
    )

    duplicates = agency_b.loc[duplicate_indices].copy()

    agency_b = pd.concat(
        [agency_b, duplicates],
        ignore_index=True,
    )

    metadata["duplicate_policy_ids"] = (
        duplicates["policy_id"].tolist()
    )

    # E. Introduce unmatched policies

    unmatched_records = []

    for i in range(UNMATCHED_POLICY_COUNT):

        policy_number = 2001 + i

        record = {
            "policy_id": f"POL{policy_number}",
            "customer_name": rng.choice(
                ["William Clark", "Isabella Lewis", "Ethan Walker"]
            ),
            "carrier": rng.choice(
                ["ABC Insurance", "XYZ Insurance"]
            ),
            "premium": round(rng.uniform(5000, 25000), 2),
            "status": "Active",
            "effective_date": "2026-03-01",
            "expiration_date": "2027-03-01",
        }

        unmatched_records.append(record)

        metadata["unmatched_policy_ids"].append(
            record["policy_id"]
        )

    unmatched_df = pd.DataFrame(unmatched_records)

    agency_b = pd.concat(
        [agency_b, unmatched_df],
        ignore_index=True,
    )

    # F. Standardize status representation

    agency_b["status"] = agency_b["status"].replace(
        {
            "Active": "In Force",
            "Expired": "Terminated",
        }
    )

    return agency_b, metadata


# 6. VALIDATE GENERATED DATA

def validate_generation(base, agency_a, agency_b, metadata):

    assert len(base) == BASE_POLICY_COUNT
    assert len(agency_a) == BASE_POLICY_COUNT

    assert len(agency_b) == (
        BASE_POLICY_COUNT
        + DUPLICATE_COUNT
        + UNMATCHED_POLICY_COUNT
    )

    assert len(metadata["premium_mismatch_policy_ids"]) == (
        PREMIUM_MISMATCH_COUNT
    )

    assert len(metadata["duplicate_policy_ids"]) == (
        DUPLICATE_COUNT
    )

    assert len(metadata["missing_customer_policy_ids"]) == (
        MISSING_CUSTOMER_COUNT
    )

    assert len(metadata["unmatched_policy_ids"]) == (
        UNMATCHED_POLICY_COUNT
    )

    assert base["policy_id"].is_unique

    print("All generation validations passed!")


# 7. SAVE GENERATED DATA

def save_datasets(agency_a, agency_b, metadata):

    AGENCY_A_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    AGENCY_B_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    agency_a.to_csv(AGENCY_A_PATH, index=False)

    agency_b.to_csv(AGENCY_B_PATH, index=False)

    with open(METADATA_PATH, "w") as file:
        json.dump(metadata, file, indent=4)


# 8. MAIN EXECUTION

def main():

    rng = random.Random(RANDOM_SEED)

    base_policies = generate_base_policies(rng)

    agency_a = create_agency_a(base_policies)

    agency_b, metadata = create_agency_b(
        base_policies,
        rng,
    )

    validate_generation(
        base_policies,
        agency_a,
        agency_b,
        metadata,
    )

    save_datasets(
        agency_a,
        agency_b,
        metadata,
    )

    print("\nSynthetic data generated successfully!")

    print(f"Base policies: {len(base_policies)}")
    print(f"Agency A records: {len(agency_a)}")
    print(f"Agency B records: {len(agency_b)}")

    print(
        "Premium mismatches:",
        len(metadata["premium_mismatch_policy_ids"]),
    )

    print(
        "Duplicate records:",
        len(metadata["duplicate_policy_ids"]),
    )

    print(
        "Missing customer names:",
        len(metadata["missing_customer_policy_ids"]),
    )

    print(
        "Unmatched policies:",
        len(metadata["unmatched_policy_ids"]),
    )

    print("\nOutput files:")
    print(AGENCY_A_PATH)
    print(AGENCY_B_PATH)
    print(METADATA_PATH)


if __name__ == "__main__":
    main()
