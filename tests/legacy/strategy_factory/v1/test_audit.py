import pandas as pd

from strategy_factory.audit import audit_bar_data, audit_model_dataset


def test_bar_audit_detects_duplicate():
    frame = pd.DataFrame(
        [
            {"timestamp_utc": "2026-01-01T00:00:00Z", "symbol": "NQ", "open": 1, "high": 2, "low": 0, "close": 1},
            {"timestamp_utc": "2026-01-01T00:00:00Z", "symbol": "NQ", "open": 1, "high": 2, "low": 0, "close": 1},
        ]
    )
    report = audit_bar_data(frame)
    assert not report.passed


def test_dataset_audit_rejects_outcome_feature():
    frame = pd.DataFrame(
        {
            "event_id": ["E"],
            "candidate_id": ["C"],
            "known_time_utc": ["2026-01-01T00:00:00Z"],
            "snapshot_time_utc": ["2026-01-01T00:00:00Z"],
            "label_end_time_utc": ["2026-01-01T01:00:00Z"],
            "net_r": [1.0],
        }
    )
    report = audit_model_dataset(frame, feature_columns=["net_r"])
    assert not report.passed
