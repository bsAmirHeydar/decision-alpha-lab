import pandas as pd

from strategy_factory.validation.folds import PurgedWalkForwardSplitter


def test_purge_removes_training_labels_overlapping_test():
    frame = pd.DataFrame(
        {
            "known_time_utc": pd.date_range("2026-01-01", periods=12, freq="D", tz="UTC"),
            "label_end_time_utc": pd.date_range("2026-01-02", periods=12, freq="D", tz="UTC"),
            "market_event_cluster_id": [f"C{i}" for i in range(12)],
        }
    )
    splitter = PurgedWalkForwardSplitter(n_splits=2, test_size=3, min_train_size=6, embargo="0s")
    folds = list(splitter.split(frame))
    assert folds
    for fold in folds:
        train = frame.iloc[fold.train_index]
        test = frame.iloc[fold.test_index]
        assert train["label_end_time_utc"].max() < test["known_time_utc"].min()
        assert set(train["market_event_cluster_id"]).isdisjoint(test["market_event_cluster_id"])
