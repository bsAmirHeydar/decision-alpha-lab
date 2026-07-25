from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from strategy_factory_rthp_train_activation_v1.config import load_activation_config
from strategy_factory_rthp_train_activation_v1.pipeline import RTHPTrainActivationPipeline, verify_run_root


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(root).as_posix().encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def test_one_shot_smoke_train_passes_without_mutating_context_or_engine(smoke_config_path: Path, repo_root: Path):
    context_root = repo_root / "lab" / "11_strategy_factory" / "contexts" / "CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1"
    engine_roots = [
        repo_root / "lab" / "11_strategy_factory" / "python" / "strategy_factory_contexts_v3",
        repo_root / "lab" / "11_strategy_factory" / "python" / "strategy_factory_trainers_v3",
        repo_root / "lab" / "11_strategy_factory" / "python" / "strategy_factory_dataset_v3",
    ]
    before_context = _tree_hash(context_root)
    before_engines = [_tree_hash(path) for path in engine_roots]
    config = load_activation_config(smoke_config_path)
    result = RTHPTrainActivationPipeline(config, repo_root).run()
    assert result["status"] == "PASS"
    assert result["passed_task_count"] == 2
    assert result["engine_modified"] is False
    assert result["canonical_context_modified"] is False
    assert result["entry_treatment_execution_created"] is False
    assert result["final_test_sealed"] is True
    assert _tree_hash(context_root) == before_context
    assert [_tree_hash(path) for path in engine_roots] == before_engines
    verification = verify_run_root(config.output_root)
    assert verification["status"] == "PASS"
    manifest = json.loads((config.output_root / "run_manifest.json").read_text(encoding="utf-8"))
    assert manifest["final_test_sealed"] is True
    assert (config.output_root / "batch" / "immutable_batch_manifest.json").is_file()


def test_existing_run_directory_is_never_overwritten(smoke_config_path: Path, repo_root: Path):
    config = load_activation_config(smoke_config_path)
    config.output_root.mkdir(parents=True)
    with pytest.raises(FileExistsError):
        RTHPTrainActivationPipeline(config, repo_root).run()


def test_protected_output_tree_is_rejected(smoke_config_path: Path, repo_root: Path):
    raw = json.loads(smoke_config_path.read_text(encoding="utf-8"))
    raw["output_root"] = (repo_root / "lab" / "11_strategy_factory" / "python" / "forbidden_run").as_posix()
    smoke_config_path.write_text(json.dumps(raw), encoding="utf-8")
    config = load_activation_config(smoke_config_path)
    with pytest.raises(ValueError, match="protected source tree"):
        RTHPTrainActivationPipeline(config, repo_root)
