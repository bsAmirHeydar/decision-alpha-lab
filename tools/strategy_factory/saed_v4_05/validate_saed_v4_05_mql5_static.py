from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
INCLUDE = ROOT / "mql5/Include/AlphaLab/StrategyFactory/SAEDV4SemanticHypergraph"
EXPERT = ROOT / "mql5/Experts/AlphaLab/StrategyFactory/Diagnostics"
files = sorted(INCLUDE.glob("*.mqh")) + sorted(EXPERT.glob("EXP_SAED_V4_05_*.mq5"))
if len(files) < 12:
    raise SystemExit("V4-05 MQL5 mirror is incomplete")
forbidden = (
    "OrderSend(",
    "OrderSendAsync(",
    "CTrade",
    "trade.Buy(",
    "trade.Sell(",
    "PositionOpen(",
    "PositionClose(",
    "WebRequest(",
    "SocketCreate(",
    "LongToString(",
)
errors = []
for path in files:
    text = path.read_text(encoding="utf-8")
    for token in forbidden:
        if token in text:
            errors.append(f"{path.relative_to(ROOT)} contains {token}")
    if path.suffix == ".mqh":
        if "#ifndef" not in text or "#define" not in text or not text.rstrip().endswith("#endif"):
            errors.append(f"{path.relative_to(ROOT)} lacks a complete include guard")
    if re.search(r"StringTo(?:Upper|Lower)\s*\([^;]+\)\s*[+.]", text):
        errors.append(f"{path.relative_to(ROOT)} treats mutating string case function as a value")
if errors:
    raise SystemExit("; ".join(errors))
print(f"static-validated {len(files)} diagnostic-only MQL5 files")
