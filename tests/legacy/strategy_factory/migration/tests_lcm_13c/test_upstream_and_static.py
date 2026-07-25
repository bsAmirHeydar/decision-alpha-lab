import json
import shutil

import pytest

from tools.strategy_factory.lcm.lcm_13c.constants import UPSTREAM_CUTOVER_ROOT
from tools.strategy_factory.lcm.lcm_13c.schema_validation import validate_schema_directory
from tools.strategy_factory.lcm.lcm_13c.service import LCM13CRollbackClosureService
from tools.strategy_factory.lcm.lcm_13c.static_validation import static_validate


def test_schema_directory(repo_root):
    assert validate_schema_directory(
        repo_root / "registry/legacy_context_migration/lcm_13c/schemas/v1"
    ) == []


def test_static_authority_boundary(repo_root):
    assert static_validate(repo_root / "src/engine/tooling/strategy_factory/lcm/lcm_13c") == []


def test_tampered_upstream_handoff_is_rejected(repo_root, tmp_path):
    clone = tmp_path / "repo"
    upstream = clone / UPSTREAM_CUTOVER_ROOT
    upstream.mkdir(parents=True)
    source = repo_root / UPSTREAM_CUTOVER_ROOT
    for name in (
        "LCM13B_TO_LCM13C_HANDOFF.json",
        "cutover_receipt.json",
        "consumer_wave_registry.json",
        "rollback_manifest.json",
    ):
        shutil.copy2(source / name, upstream / name)
    handoff = json.loads((upstream / "LCM13B_TO_LCM13C_HANDOFF.json").read_text())
    handoff["cutover_consumer_count"] += 1
    (upstream / "LCM13B_TO_LCM13C_HANDOFF.json").write_text(
        json.dumps(handoff, indent=2, sort_keys=True) + "\n"
    )
    with pytest.raises(ValueError, match="UPSTREAM_DIGEST_INVALID"):
        LCM13CRollbackClosureService(clone).build(tmp_path / "out")
