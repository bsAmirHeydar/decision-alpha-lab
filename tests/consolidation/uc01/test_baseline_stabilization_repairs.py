import ast
from pathlib import Path

import pytest

from tools.repository_paths import resolve_repository_path

REPAIRED_PATHS = (
    "lab/11_strategy_factory/python/saed_v4_anytime_valid_online_fdr/cli.py",
    "lab/11_strategy_factory/python/saed_v4_complete_search_exposure_ledger/cli.py",
    "lab/11_strategy_factory/python/saed_v4_decision_focused_treatment_selection/cli.py",
    "lab/11_strategy_factory/python/saed_v4_foundation_model_adapters/cli.py",
    "lab/11_strategy_factory/python/saed_v4_generative_path_stress_lab/cli.py",
    "lab/11_strategy_factory/python/saed_v4_independent_multi_lab_replication/cli.py",
    "lab/11_strategy_factory/python/saed_v4_mechanistic_interpretability/cli.py",
    "lab/11_strategy_factory/python/saed_v4_multimodal_views/cli.py",
    "lab/11_strategy_factory/python/saed_v4_offline_policy_research/cli.py",
    "lab/11_strategy_factory/python/saed_v4_self_supervised_pretraining/serialization.py",
    "tools/strategy_factory/generate_uce_i13_vectors.py",
)


@pytest.mark.parametrize("relative_path", REPAIRED_PATHS)
def test_baseline_stabilization_file_parses(relative_path: str) -> None:
    root = Path(__file__).resolve().parents[3]
    path = resolve_repository_path(root, relative_path, require_exists=True)
    text = path.read_text(encoding="utf-8")
    ast.parse(text, filename=relative_path)
    assert "+'\\n'" in text or '+"\\n"' in text or "'\\n'.join" in text
