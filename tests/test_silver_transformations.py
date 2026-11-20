import pandas as pd

from src.transformations.silver_transformations import (
    standardize_policy_id,
    normalize_status,
)


# Policy ID tests

def test_policy_id_with_hyphen():
    assert standardize_policy_id("POL-1001") == "POL-1001"


def test_policy_id_without_hyphen():
    assert standardize_policy_id("POL1001") == "POL-1001"


def test_policy_id_with_whitespace_and_lowercase():
    assert standardize_policy_id(" pol1002 ") == "POL-1002"


def test_missing_policy_id():
    assert standardize_policy_id(None) is None


# Status tests

def test_active_status():
    assert normalize_status("Active") == "Active"


def test_in_force_status():
    assert normalize_status("In Force") == "Active"


def test_pending_status():
    assert normalize_status("Pending") == "Pending"


def test_expired_status():
    assert normalize_status("Expired") == "Terminated"


def test_terminated_status():
    assert normalize_status("Terminated") == "Terminated"


def test_status_with_whitespace_and_lowercase():
    assert normalize_status(" in force ") == "Active"


def test_missing_status():
    assert normalize_status(None) is None