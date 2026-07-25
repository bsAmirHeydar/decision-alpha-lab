from tools.repository_paths import find_repository_root
from pathlib import Path

ROOT = find_repository_root(__file__)
include_dir = ROOT / "mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_25"
expert_dir = ROOT / "mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_25"
files = sorted(include_dir.glob("*.mqh")) + sorted(expert_dir.glob("*.mq5"))
assert len(files) == 22, len(files)
forbidden = ["OrderSend(", "OrderSendAsync(", "CTrade", ".Buy(", ".Sell(", "WebRequest(", "SocketCreate("]
for path in files:
    text = path.read_text(encoding="utf-8")
    assert "SAED" in text and "V4_25" in path.as_posix(), path
    assert not any(token in text for token in forbidden), path
    if path.suffix == ".mqh":
        assert "#ifndef" in text and "#define" in text and "#endif" in text, path
    else:
        assert "#property strict" in text and "void OnTick" in text, path
print(f"V4-25 MQL5 static validation passed: {len(files)} files; MetaEditor compile pending_local_windows")
