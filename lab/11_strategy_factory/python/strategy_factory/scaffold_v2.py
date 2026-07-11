"""Generate a thin vertical-slice V2 anatomy plugin packet."""
from __future__ import annotations

import json
from pathlib import Path


DOCTRINE = """# Anatomy Doctrine\n\n## Market fact\n\nDefine the observable fact without entry, stop, target, or outcome language.\n\n## Known-time contract\n\nState event time, known time, confirmation time, and any closed-bar requirements.\n\n## Identity\n\nDefine stable identity fields and the underlying market-event cluster rule.\n\n## Lifecycle\n\nDefine candidate, confirmed, invalidated, expired, consumed, and retired states.\n\n## Matched null\n\nDefine the baseline that preserves session, volatility, holding horizon, and confirmation while removing the anatomy condition.\n\n## Kill criteria\n\nState the evidence that permanently rejects this hypothesis version.\n"""

ADAPTER = '''"""V2 anatomy adapter skeleton."""\nfrom __future__ import annotations\n\nfrom typing import Any, Mapping\n\nfrom strategy_factory.contracts import AnatomyEvent, Direction\nfrom strategy_factory.plugins import PluginDescriptor\n\n\nclass AnatomyAdapter:\n    descriptor = PluginDescriptor(\n        plugin_id="__STRATEGY_ID___adapter",\n        version="1.0.0",\n        kind="anatomy_adapter",\n        deterministic=True,\n        thread_safe=True,\n        fast_path_safe=True,\n        capabilities=("emit_event", "known_time"),\n    )\n\n    def emit(self, raw_event: Mapping[str, Any]) -> AnatomyEvent:\n        raise NotImplementedError("Map the existing anatomy engine output to AnatomyEvent")\n'''

FEATURES = '''"""Strategy-specific feature-provider skeleton."""\nfrom __future__ import annotations\n\nfrom strategy_factory.context import MappingFeatureProvider\nfrom strategy_factory.plugins import PluginDescriptor\n\n\ndef build_providers():\n    return [\n        MappingFeatureProvider(\n            descriptor=PluginDescriptor(\n                plugin_id="__STRATEGY_ID___features",\n                version="1.0.0",\n                kind="feature_provider",\n                capabilities=("online", "batch"),\n            ),\n            feature_names=("anatomy_quality",),\n            dependencies=(),\n            ttl_seconds=1.0,\n            required=True,\n            compute_fn=lambda event, resolved, market: {\n                "anatomy_quality": market["anatomy_quality"]\n            },\n        )\n    ]\n'''

TEST = '''from datetime import datetime, timezone\n\nimport pytest\n\nfrom adapter import AnatomyAdapter\n\n\ndef test_adapter_requires_real_mapping():\n    with pytest.raises(NotImplementedError):\n        AnatomyAdapter().emit({})\n'''


def scaffold_strategy_v2(strategy_id: str, output_root: str | Path, *, force: bool = False) -> Path:
    safe = strategy_id.strip().lower().replace(" ", "_")
    if not safe or any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789_-" for ch in safe):
        raise ValueError("strategy_id must contain only ASCII letters, digits, underscore, or hyphen")
    root = Path(output_root).expanduser().resolve() / safe
    if root.exists() and any(root.iterdir()) and not force:
        raise FileExistsError(f"strategy directory already exists and is not empty: {root}")
    (root / "tests").mkdir(parents=True, exist_ok=True)
    (root / "fixtures").mkdir(parents=True, exist_ok=True)
    (root / "ANATOMY_DOCTRINE.md").write_text(DOCTRINE, encoding="utf-8")
    (root / "adapter.py").write_text(ADAPTER.replace("__STRATEGY_ID__", safe), encoding="utf-8")
    (root / "features.py").write_text(FEATURES.replace("__STRATEGY_ID__", safe), encoding="utf-8")
    (root / "tests" / "test_adapter.py").write_text(TEST, encoding="utf-8")
    spec = {
        "strategy": {
            "id": safe,
            "version": "0.1.0",
            "owner": "Decision Alpha Lab",
            "thesis": "REPLACE_ME",
            "null_hypothesis": "REPLACE_ME",
        },
        "context": {
            "providers": [],
            "feature_vectors": {
                "quality": {
                    "version": "1.0.0",
                    "names": ["anatomy_quality", "risk_distance"],
                    "defaults": [0.0, 1.0],
                }
            },
        },
        "decision": {
            "max_candidates_per_event": 2,
            "candidate_templates": [
                {
                    "id": "market_structural_1_5r",
                    "entry": "market_on_confirmation",
                    "stop": "anatomy_invalidation",
                    "exit": "fixed_r",
                    "priority": 0,
                    "parameters": {"reward_r": 1.5},
                }
            ],
            "models": [],
            "model_routes": [],
            "utility_weights": {"expected_r": 1.0},
            "abstention": {
                "minimum_probability": 0.5,
                "minimum_expected_r": 0.0,
                "required_context_keys": ["anatomy_quality"],
            },
        },
        "runtime": {
            "fallback_mode": "abstain",
            "latency_budget_ms": {"context": 3.0, "candidates": 1.0, "models": 1.0, "ranking": 0.5, "total": 8.0},
        },
        "metadata": {"mode": "research", "authoritative_execution": False},
    }
    (root / "strategy_v2.json").write_text(json.dumps(spec, indent=2), encoding="utf-8")
    (root / "fixtures" / "README.md").write_text(
        "# Fixtures\n\nAdd positive, negative, invalid, boundary, stale, DST, and replay fixtures.\n",
        encoding="utf-8",
    )
    return root
