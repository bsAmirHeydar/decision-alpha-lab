"""Reference end-to-end Strategy Factory pipeline orchestration."""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from .adapters.csv_adapter import CsvAnatomyAdapter
from .anti_overfit import best_trade_removal, cluster_bootstrap, cost_stress
from .artifacts import build_run_manifest, object_sha256, write_frame, write_json
from .candidate_engine import generate_candidates
from .costs import CostModel
from .dataset import assemble_model_dataset, candidates_to_frame, events_to_frame, snapshots_to_frame
from .labels import add_event_ranks, add_standard_labels, outcomes_to_frame
from .manifest import StrategyManifest
from .simulation import SimulationPolicy, simulate_many
from .statistics import summarize


class StrategyPipeline:
    """Small reference orchestrator; production deployments may use a job runner.

    The class intentionally keeps each artifact materialized.  No hidden
    in-memory transformation is allowed to become authoritative without a
    versioned artifact and hash.
    """

    def __init__(self, manifest: StrategyManifest, run_root: str | Path) -> None:
        self.manifest = manifest
        self.run_root = Path(run_root)
        self.run_root.mkdir(parents=True, exist_ok=True)

    def run_reference_csv(
        self,
        *,
        event_source: str | Path,
        feature_source: str | Path,
        bars_by_symbol: Mapping[str, pd.DataFrame],
        cost_models: Mapping[str, CostModel] | None = None,
    ) -> Mapping[str, Any]:
        adapter = CsvAnatomyAdapter()
        event_frame = pd.read_csv(event_source)
        feature_frame = pd.read_csv(feature_source)
        events = list(adapter.emit_events(event_frame, self.manifest))
        features_by_event = feature_frame.set_index("event_id", drop=False)
        snapshots = []
        candidates = []
        for event in events:
            if event.event_id not in features_by_event.index:
                raise KeyError(f"missing feature row for event {event.event_id}")
            feature_row = features_by_event.loc[event.event_id]
            if isinstance(feature_row, pd.DataFrame):
                raise ValueError(f"duplicate feature rows for event {event.event_id}")
            snapshot = adapter.build_snapshot(event, feature_row, self.manifest, event.confirmation_time_utc)
            snapshots.append(snapshot)
            candidates.extend(generate_candidates(event, snapshot.as_flat_dict(), self.manifest))

        costs = dict(cost_models or {})
        outcomes = simulate_many(
            candidates,
            dict(bars_by_symbol),
            costs,
            policy=SimulationPolicy(intrabar_ambiguity="stop_first"),
        )

        events_df = events_to_frame(events)
        snapshots_df = snapshots_to_frame(snapshots)
        candidates_df = candidates_to_frame(candidates)
        outcomes_df = outcomes_to_frame(outcomes)
        labels_df = add_event_ranks(add_standard_labels(outcomes_to_frame(outcomes)))
        model_df = assemble_model_dataset(events_df, snapshots_df, candidates_df, outcomes_df)
        model_df = model_df.merge(
            labels_df[[col for col in labels_df.columns if col.startswith("label_") or col in {"candidate_id", "event_candidate_rank", "event_best_candidate"}]],
            on="candidate_id",
            how="left",
            validate="one_to_one",
        )

        write_frame(self.run_root / "events.parquet", events_df)
        write_frame(self.run_root / "snapshots.parquet", snapshots_df)
        write_frame(self.run_root / "candidates.parquet", candidates_df)
        write_frame(self.run_root / "outcomes.parquet", outcomes_df)
        write_frame(self.run_root / "model_dataset.parquet", model_df)

        performance = summarize(model_df)
        cluster_key = self.manifest.section("validation").get("cluster_key", "market_event_cluster_id")
        anti: dict[str, Any] = {
            "best_trade_removal": best_trade_removal(model_df["net_r"].fillna(0.0)).to_dict(orient="records"),
        }
        if cluster_key in model_df.columns and model_df[cluster_key].notna().any():
            anti["cluster_bootstrap"] = cluster_bootstrap(
                model_df.dropna(subset=[cluster_key]),
                value_col="net_r",
                cluster_col=str(cluster_key),
                iterations=500,
            )
        cost_series = model_df.get("spread_cost_r", pd.Series(0.0, index=model_df.index)).fillna(0.0)
        anti["cost_stress"] = cost_stress(model_df["net_r"].fillna(0.0), cost_series).to_dict(orient="records")

        run_id = self.run_root.name
        manifest = build_run_manifest(
            run_id=run_id,
            repo_root=self.run_root,
            strategy_id=self.manifest.strategy_id,
            strategy_version=self.manifest.version,
            manifest_hash=self.manifest.manifest_hash,
            dataset_hash=object_sha256(model_df.to_dict(orient="records")),
            candidate_set_hash=object_sha256(candidates_df.to_dict(orient="records")),
            label_set_hash=object_sha256(labels_df.to_dict(orient="records")),
            status="research_complete",
        )
        write_json(self.run_root / "run_manifest.json", manifest)
        write_json(self.run_root / "statistics.json", performance.to_dict())
        write_json(self.run_root / "anti_overfit.json", anti)
        return {
            "run_manifest": manifest,
            "performance": performance.to_dict(),
            "anti_overfit": anti,
            "artifact_root": str(self.run_root),
        }
