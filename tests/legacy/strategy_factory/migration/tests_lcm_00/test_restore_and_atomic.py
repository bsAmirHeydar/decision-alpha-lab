from pathlib import Path
import pytest

from src.engine.tooling.strategy_factory.lcm.lcm_00.errors import DestinationConflict
from src.engine.tooling.strategy_factory.lcm.lcm_00.io import atomic_directory


def test_reference_restore_rehearsal_passed(baseline_root):
    import json
    report=json.loads((baseline_root/"restoration/restore_rehearsal_report.json").read_text(encoding="utf-8"))
    assert report["passed"] is True
    assert report["mismatch_count"] == 0
    assert report["copied_record_count"] == report["verified_record_count"]


def test_nonempty_destination_rejected(tmp_path):
    dest=tmp_path/"dest"; dest.mkdir(); (dest/"x").write_text("x")
    with pytest.raises(DestinationConflict):
        with atomic_directory(dest):
            pass


def test_atomic_directory_publishes_complete_tree(tmp_path):
    dest=tmp_path/"dest"
    with atomic_directory(dest) as stage:
        (stage/"a").write_text("ok")
    assert (dest/"a").read_text() == "ok"
