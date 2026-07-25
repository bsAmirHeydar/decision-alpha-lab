import json
import shutil

import pytest

from tools.strategy_factory.lcm.lcm_14a.constants import UPSTREAM_CLOSURE_ROOT
from tools.strategy_factory.lcm.lcm_14a.schema_validation import validate_schema_directory
from tools.strategy_factory.lcm.lcm_14a.service import LCM14ADeprecationRedirectService
from tools.strategy_factory.lcm.lcm_14a.static_validation import static_validate


def test_schema_directory(repo_root):
    assert validate_schema_directory(repo_root / "registry/legacy_context_migration/lcm_14a/schemas/v1") == []


def test_static_authority_boundary(repo_root):
    assert static_validate(repo_root / "src/engine/tooling/strategy_factory/lcm/lcm_14a") == []


def test_tampered_upstream_handoff_is_rejected(repo_root, tmp_path):
    clone = tmp_path / "repo"
    upstream = clone / UPSTREAM_CLOSURE_ROOT
    upstream.mkdir(parents=True)
    source = repo_root / UPSTREAM_CLOSURE_ROOT
    for name in ("LCM13C_TO_LCM14A_HANDOFF.json", "deprecation_candidate_registry.json"):
        shutil.copy2(source / name, upstream / name)
    handoff = json.loads((upstream / "LCM13C_TO_LCM14A_HANDOFF.json").read_text())
    handoff["deprecation_candidate_count"] += 1
    (upstream / "LCM13C_TO_LCM14A_HANDOFF.json").write_text(json.dumps(handoff, indent=2, sort_keys=True) + "\n")
    with pytest.raises(ValueError, match="UPSTREAM_DIGEST_INVALID"):
        LCM14ADeprecationRedirectService(clone).build(tmp_path / "out")
