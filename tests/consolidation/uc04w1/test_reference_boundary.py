from __future__ import annotations

from pathlib import Path

from tools.consolidation.uc04w1.characterize import REFERENCE_HEADER, SELF_TEST
from tools.consolidation.uc04w1.verify import REFERENCE_FORBIDDEN_TOKENS


def test_reference_implementation_is_test_only_and_pure(repo_root: Path) -> None:
    assert REFERENCE_HEADER.as_posix().startswith("mql5/Tests/")
    text = (repo_root / REFERENCE_HEADER).read_text(encoding="utf-8-sig")
    assert "TimeToStruct(value, dt);" in text
    assert 'StringFormat("%04d.%02d.%02d %02d:%02d:%02d"' in text
    for token in REFERENCE_FORBIDDEN_TOKENS:
        assert token not in text


def test_native_self_test_has_no_order_network_or_chart_authority(repo_root: Path) -> None:
    text = (repo_root / SELF_TEST).read_text(encoding="utf-8-sig")
    assert "#property strict" in text
    assert "FILE_COMMON" in text
    assert "UC04-W1A SELFTEST PASS" in text
    for token in ("OrderSend", "CTrade", "PositionOpen", "WebRequest", "ObjectCreate"):
        assert token not in text


def test_capture_harness_uses_isolated_workspace(repo_root: Path) -> None:
    text = (repo_root / "tools/consolidation/uc04w1/capture_native_acceptance.ps1").read_text(encoding="utf-8-sig")
    assert "compile_workspace" in text
    assert "Copy-Item" in text
    assert "tracked_source_mutation = $false" in text
    assert "0\\s+errors?" in text
    assert "0\\s+warnings?" in text
