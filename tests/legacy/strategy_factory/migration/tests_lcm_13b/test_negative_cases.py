from __future__ import annotations
import json
import pytest
from src.engine.tooling.strategy_factory.lcm.lcm_13b.service import LCM13BConsumerWaveCutoverService, UPSTREAM_HANDOFF

def test_tampered_upstream_handoff_is_rejected(repo_root, tmp_path):
    clone = tmp_path / "repo"
    path = clone / UPSTREAM_HANDOFF
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads((repo_root / UPSTREAM_HANDOFF).read_text(encoding="utf-8"))
    data["consumer_counts"]["total"] += 1
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="UPSTREAM_HANDOFF_DIGEST_INVALID"):
        LCM13BConsumerWaveCutoverService(clone).build(tmp_path / "out")
