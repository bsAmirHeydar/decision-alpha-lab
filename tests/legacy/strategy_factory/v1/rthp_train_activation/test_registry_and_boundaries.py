from __future__ import annotations

import json
from pathlib import Path

from strategy_factory_rthp_train_activation_v1 import RTHPTrainActivationPipeline


def test_registration_is_context_owned(repo_root: Path):
    path = repo_root / "registry" / "strategy_factory" / "contexts" / "rthp" / "v1" / "rthp_train_activation_registration.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    assert value["python_import"] == "strategy_factory_rthp_train_activation_v1:RTHPTrainActivationPipeline"
    assert value["shared_engine_change_allowed"] is False
    assert value["canonical_context_change_allowed"] is False
    assert value["network_fetch_allowed"] is False
    assert value["status"] == "READY"


def test_activation_namespace_is_separate_from_shared_engines():
    module = RTHPTrainActivationPipeline.__module__
    assert module.startswith("strategy_factory_rthp_train_activation_v1")
    assert "strategy_factory_trainers_v3" not in module
    assert "strategy_factory_contexts_v3" not in module
