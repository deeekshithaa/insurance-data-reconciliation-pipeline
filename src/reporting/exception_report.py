import pandas as pd


def generate_exception_summary(df):
    """Generate summary metrics for the exception management dataset."""

    total_exceptions = len(df)

    status_counts = df["review_status"].value_counts().to_dict()
    priority_counts = df["priority"].value_counts().to_dict()

    resolved_count = status_counts.get("Resolved", 0)
    unresolved_count = total_exceptions - resolved_count

    resolution_rate = (
        (resolved_count / total_exceptions) * 100
        if total_exceptions > 0
        else 0
    )

    summary = {
        "total_exceptions": total_exceptions,
        "open": status_counts.get("Open", 0),
        "in_review": status_counts.get("In Review", 0),
        "resolved": resolved_count,
        "unresolved": unresolved_count,
        "high_priority": priority_counts.get("High", 0),
        "medium_priority": priority_counts.get("Medium", 0),
        "low_priority": priority_counts.get("Low", 0),
        "resolution_rate_pct": round(resolution_rate, 2),
    }

    return summary