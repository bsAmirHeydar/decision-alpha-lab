import hashlib
from pathlib import Path

from src.engine.tooling.strategy_factory.lcm.lcm_13c.service import LCM13CRollbackClosureService


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def test_clean_rebuild_is_byte_deterministic(repo_root, tmp_path):
    service = LCM13CRollbackClosureService(repo_root)
    first = service.build(tmp_path / "first")
    second = service.build(tmp_path / "second")
    assert first.closure_id == second.closure_id
    assert first.handoff_digest == second.handoff_digest
    assert first.wave_count == second.wave_count == 27
    assert first.consumer_count == second.consumer_count == 613
    assert first.blocked_consumer_count == second.blocked_consumer_count == 806
    assert first.state_record_count == second.state_record_count == 162
    assert first.event_count == second.event_count == 189
    assert tree_digest(first.output_root) == tree_digest(second.output_root)
