import hashlib
from pathlib import Path

import pytest

from tools.strategy_factory.lcm.lcm_16b import evidence as module
from tools.strategy_factory.lcm.lcm_16b.evidence import (
    _validate_approvals,
    _validate_consumers,
    _validate_metaeditor,
    _validate_parity,
    _validate_tester,
)


def _sha(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def test_metaeditor_clean_log_and_ex5(tmp_path):
    log = tmp_path / "compile.log"; log.write_text("Result: 0 errors, 0 warnings\n")
    ex5 = tmp_path / "target.ex5"; ex5.write_bytes(b"compiled")
    target = "mql5/Experts/X.mq5"
    result = _validate_metaeditor(tmp_path, {"status":"PASS","targets":[{"source_path":target,"errors":0,"warnings":0,"log_path":"compile.log","log_path_sha256":_sha(log),"ex5_path":"target.ex5","ex5_sha256":_sha(ex5)}]}, [target])
    assert result["status"] == "PASS"


def test_metaeditor_nonzero_errors_rejected(tmp_path):
    with pytest.raises(ValueError, match="not clean"):
        _validate_metaeditor(tmp_path, {"status":"PASS","targets":[{"source_path":"x","errors":1,"warnings":0}]}, ["x"])


def test_tester_requires_report_and_journal(tmp_path):
    report=tmp_path/'r.xml'; report.write_text('ok')
    with pytest.raises(ValueError, match="evidence item missing"):
        _validate_tester(tmp_path, {"status":"PASS","targets":[{"source_path":"x","result":"PASS","deterministic_replay_digest":"sha256:"+'1'*64,"report_path":"r.xml","report_path_sha256":_sha(report)}]}, ["x"])


def test_parity_requires_zero_mismatch(tmp_path):
    with pytest.raises(ValueError, match="zero mismatches"):
        _validate_parity(tmp_path, {"status":"PASS","case_count":10,"mismatch_count":1})


def test_external_consumers_require_zero_unresolved(tmp_path):
    with pytest.raises(ValueError, match="zero unresolved"):
        _validate_consumers(tmp_path, {"status":"PASS","unresolved_consumer_count":2})


def test_approvals_require_all_roles():
    status, approvals = _validate_approvals([])
    assert status == "BLOCKED"
    assert approvals == []


def test_unknown_approval_role_rejected():
    with pytest.raises(ValueError, match="unexpected"):
        _validate_approvals([{"role":"TRADER","decision":"APPROVE_PROGRAM_CLOSURE","approval_id":"A","signer":"S","evidence_digest":"sha256:"+'1'*64}])
