"""Generate the minimal plugin packet required for a new anatomy."""
from __future__ import annotations

from pathlib import Path
import json
import re


def normalize_id(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9_]+", "_", value.strip()).strip("_")
    if not normalized:
        raise ValueError("strategy id cannot be empty")
    if normalized[0].isdigit():
        normalized = "S_" + normalized
    return normalized


def scaffold_strategy(strategy_id: str, output_root: str | Path, *, force: bool = False) -> Path:
    sid = normalize_id(strategy_id)
    root = Path(output_root) / sid
    if root.exists() and any(root.iterdir()) and not force:
        raise FileExistsError(f"scaffold target is not empty: {root}")
    root.mkdir(parents=True, exist_ok=True)
    (root / "tests").mkdir(exist_ok=True)
    (root / "fixtures").mkdir(exist_ok=True)

    manifest = {
        "strategy": {
            "id": sid,
            "version": "0.1.0",
            "owner": "Decision Alpha Lab",
            "status": "draft",
            "thesis": "REPLACE_WITH_FALSIFIABLE_THESIS",
            "null_hypothesis": "REPLACE_WITH_MATCHED_NULL",
            "kill_criteria": ["REPLACE_WITH_KILL_CRITERION"],
        },
        "anatomy_adapter": {
            "type": f"{sid.lower()}_adapter",
            "version": "0.1.0",
            "known_time_field": "known_time_utc",
            "event_id_fields": ["symbol", "direction", "known_time_utc"],
        },
        "features": {
            "schema_version": "0.1.0",
            "shared": ["confirmation_close", "atr", "spread", "realized_volatility", "session_minute"],
            "strategy_specific": [],
            "forbidden": ["net_r", "mfe_r", "mae_r", "exit_reason"],
        },
        "candidate_universe": {
            "entries": ["market_on_confirmation"],
            "stops": ["anatomy_invalidation"],
            "exits": [{"id": "fixed_r", "parameters": {"reward_r": 2.0}}],
            "incompatible_policy_triplets": [],
            "max_candidates_per_event": 1,
            "explicit_allow_pruning": False,
            "default_expiration_seconds": 3600,
            "default_max_holding_seconds": 14400,
            "cost_model_id": "broker_realistic_v1",
        },
        "labels": {
            "version": "0.1.0",
            "primary": "label_net_r",
            "secondary": ["label_trade_positive", "label_mfe_r", "label_mae_r"],
            "label_horizon": "candidate_exit_or_max_holding",
            "intrabar_ambiguity": "stop_first",
        },
        "validation": {
            "splitter": "purged_walk_forward",
            "cluster_key": "market_event_cluster_id",
            "purge_by_label_end": True,
            "embargo_seconds": 86400,
            "minimum_unique_clusters": 200,
            "anti_overfit_suite": [
                "cluster_bootstrap",
                "benjamini_hochberg",
                "white_reality_check",
                "deflated_sharpe",
                "probability_of_backtest_overfitting",
                "best_trade_removal",
                "cost_stress",
                "delayed_entry_stress",
            ],
        },
        "models": {
            "baselines": ["always_trade", "logistic_regression", "ridge_regression"],
            "challengers": ["candidate_ranker"],
            "selection_metric": "cluster_level_oos_net_expectancy",
            "calibration_required": True,
            "minimum_uplift_over_baseline_r": 0.05,
        },
        "execution": {
            "paper_enabled": False,
            "live_enabled": False,
            "risk_policy": "micro_research_v1",
            "broker_adapter": "paper_broker_v1",
            "model_fallback": "skip",
            "missing_feature_action": "skip",
            "maximum_decision_latency_ms": 5000,
        },
    }
    (root / "strategy.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (root / "ANATOMY_DOCTRINE.md").write_text(
        f"# {sid} Anatomy Doctrine\n\n"
        "## Thesis\n\n## Null hypothesis\n\n## Entities and identity\n\n"
        "## States and transitions\n\n## Known-time semantics\n\n## Direction and invalidation\n\n"
        "## Duplicate and simultaneity policy\n\n## Cluster rule\n\n## Kill criteria\n\n"
        "## Golden examples and counterexamples\n",
        encoding="utf-8",
    )
    adapter = f'''from __future__ import annotations\n\nfrom datetime import datetime\nfrom typing import Any, Iterable\n\nfrom strategy_factory.adapters.base import AnatomyAdapter\nfrom strategy_factory.contracts import AnatomyEvent, FeatureSnapshot\nfrom strategy_factory.manifest import StrategyManifest\n\n\nclass {sid}Adapter(AnatomyAdapter):\n    adapter_id = "{sid.lower()}_adapter"\n    adapter_version = "0.1.0"\n\n    def emit_events(self, source: Any, manifest: StrategyManifest) -> Iterable[AnatomyEvent]:\n        raise NotImplementedError("Map the approved anatomy engine to AnatomyEvent")\n\n    def build_snapshot(\n        self, event: AnatomyEvent, source: Any, manifest: StrategyManifest, decision_time_utc: datetime\n    ) -> FeatureSnapshot:\n        raise NotImplementedError("Build only features known at decision_time_utc")\n'''
    (root / "adapter.py").write_text(adapter, encoding="utf-8")
    test = f'''from pathlib import Path\n\nfrom strategy_factory.manifest import load_manifest\n\n\ndef test_{sid.lower()}_manifest_is_valid():\n    manifest = load_manifest(Path(__file__).resolve().parents[1] / "strategy.json")\n    assert manifest.strategy_id == "{sid}"\n\n\ndef test_adapter_golden_fixtures():\n    # Replace with deterministic event and known-time fixtures.\n    assert True\n'''
    (root / "tests" / "test_contract.py").write_text(test, encoding="utf-8")
    (root / "fixtures" / "README.md").write_text(
        "# Golden fixtures\n\nAdd hand-verified normal, boundary, ambiguous, missing-data, and counterexample cases.\n",
        encoding="utf-8",
    )
    return root
