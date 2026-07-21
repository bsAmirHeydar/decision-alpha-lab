def _snapshot(root):
    import hashlib
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob("*") if p.is_file()
    }

def test_clean_rebuild_is_byte_deterministic(tmp_path):
    from pathlib import Path
    from tools.strategy_factory.lcm.lcm_13a.service import LCM13ADualRunService
    repo = Path(__file__).resolve().parents[4]
    a = LCM13ADualRunService(repo).build(tmp_path / "a").output_root
    b = LCM13ADualRunService(repo).build(tmp_path / "b").output_root
    assert _snapshot(a) == _snapshot(b)
