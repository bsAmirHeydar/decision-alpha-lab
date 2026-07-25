from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess
import sys

ROOT = find_repository_root(__file__)


def test_mql5_static_validator_passes():
    result = subprocess.run(
        [sys.executable, "src/engine/tooling/strategy_factory/saed_v4_05/validate_saed_v4_05_mql5_static.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "diagnostic-only MQL5 files" in result.stdout


def test_mql5_mirror_contains_no_execution_api():
    paths = list((ROOT / "mql5/Include/AlphaLab/StrategyFactory/SAEDV4SemanticHypergraph").glob("*.mqh"))
    paths += list((ROOT / "mql5/Experts/AlphaLab/StrategyFactory/Diagnostics").glob("EXP_SAED_V4_05_*.mq5"))
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "OrderSend(" not in text
    assert "CTrade" not in text
    assert "WebRequest(" not in text
