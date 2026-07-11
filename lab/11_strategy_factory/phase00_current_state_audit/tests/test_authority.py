from __future__ import annotations

from pathlib import Path

from sf_phase00.authority import scan_execution_authority


def _repo(tmp_path: Path) -> Path:
    (tmp_path / "lab").mkdir()
    (tmp_path / "docs").mkdir()
    return tmp_path


def test_comment_only_tokens_are_not_authority(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    (root / "lab" / "safe.py").write_text("# mt5.order_send(request)\n", encoding="utf-8")
    assert scan_execution_authority(root) == []


def test_executable_order_send_is_critical(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    (root / "lab" / "unsafe.py").write_text("result = mt5.order_send(request)\n", encoding="utf-8")
    findings = scan_execution_authority(root)
    assert len(findings) == 1
    assert findings[0].token == "PY_MT5_ORDER_SEND"
    assert findings[0].severity.value == "CRITICAL"
