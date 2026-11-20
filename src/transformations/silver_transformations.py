import re
import pandas as pd


def standardize_policy_id(policy_id):
    """
    Standardize policy IDs into the format POL-1234.
    """

    if pd.isna(policy_id):
        return None

    policy_id = str(policy_id).strip().upper()

    digits = re.sub(r"[^0-9]", "", policy_id)

    if not digits:
        return policy_id

    return f"POL-{digits}"


def normalize_status(status):
    """
    Normalize equivalent insurance statuses.
    """

    if pd.isna(status):
        return None

    status = str(status).strip().lower()

    status_mapping = {
        "active": "Active",
        "in force": "Active",
        "pending": "Pending",
        "expired": "Terminated",
        "terminated": "Terminated",
    }

    return status_mapping.get(status, status.title())