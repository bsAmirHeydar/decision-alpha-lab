from __future__ import annotations
import hashlib
from pathlib import Path
from src.engine.tooling.strategy_factory.lcm.lcm_13b.service import LCM13BConsumerWaveCutoverService

def tree_digest(root: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        h.update(path.relative_to(root).as_posix().encode())
        h.update(b"\0")
        h.update(path.read_bytes())
        h.update(b"\0")
    return h.hexdigest()

def test_clean_rebuild_is_byte_deterministic(repo_root, tmp_path):
    service = LCM13BConsumerWaveCutoverService(repo_root)
    first = service.build(tmp_path / "first")
    second = service.build(tmp_path / "second")
    assert first.cutover_id == second.cutover_id
    assert first.handoff_digest == second.handoff_digest
    assert tree_digest(first.output_root) == tree_digest(second.output_root)
