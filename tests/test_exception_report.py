from src.reporting.exception_report import generate_exception_summary


def test_generate_exception_summary():
    sample_data = [
        {"priority": "High", "review_status": "Resolved"},
        {"priority": "High", "review_status": "Open"},
        {"priority": "Medium", "review_status": "Open"},
        {"priority": "Medium", "review_status": "In Review"},
    ]

    import pandas as pd

    df = pd.DataFrame(sample_data)

    summary = generate_exception_summary(df)

    assert summary["total_exceptions"] == 4
    assert summary["open"] == 2
    assert summary["in_review"] == 1
    assert summary["resolved"] == 1
    assert summary["unresolved"] == 3
    assert summary["high_priority"] == 2
    assert summary["medium_priority"] == 2
    assert summary["low_priority"] == 0
    assert summary["resolution_rate_pct"] == 25.0