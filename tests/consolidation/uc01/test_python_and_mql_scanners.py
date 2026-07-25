from pathlib import Path

from tools.consolidation.uc01.mql5_scan import scan_mql5
from tools.consolidation.uc01.python_scan import scan_python


def test_python_scanner_records_symbols_imports_and_tests(tmp_path: Path) -> None:
    path = tmp_path / "tests" / "test_sample.py"
    path.parent.mkdir(parents=True)
    path.write_text(
        "import json\nfrom pathlib import Path\nclass TestThing:\n    def test_ok(self):\n        return Path('.')\n",
        encoding="utf-8",
    )
    result = scan_python(tmp_path, ["tests/test_sample.py"])
    names = {row["name"] for row in result["symbols"]}
    assert {"TestThing", "test_ok"}.issubset(names)
    assert len(result["imports"]) == 2
    assert len(result["tests"]) == 2
    assert not result["issues"]


def test_python_scanner_records_syntax_issue(tmp_path: Path) -> None:
    path = tmp_path / "bad.py"
    path.write_text("def broken(:\n", encoding="utf-8")
    result = scan_python(tmp_path, ["bad.py"])
    assert result["issues"][0]["issue"] == "syntax_error"


def test_mql5_scanner_records_authority_and_include(tmp_path: Path) -> None:
    path = tmp_path / "mql5" / "Experts" / "Sample.mq5"
    path.parent.mkdir(parents=True)
    path.write_text(
        '#include <Trade/Trade.mqh>\ninput int Period=5;\nvoid OnTick(){ CTrade trade; trade.PositionOpen("X",0,1,0,0,0); }\n',
        encoding="utf-8",
    )
    result = scan_mql5(tmp_path, ["mql5/Experts/Sample.mq5"])
    assert result["includes"][0]["target_include"] == "Trade/Trade.mqh"
    assert any(row["kind"] == "function" and row["name"] == "OnTick" for row in result["symbols"])
    kinds = {row["authority_kind"] for row in result["authority"]}
    assert "trade_class" in kinds
    assert "position_mutation" in kinds
