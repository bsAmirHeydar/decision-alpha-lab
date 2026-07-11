from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
paths = [
    root / "mql5/Include/AlphaLab/StrategyFactory/Generation",
    root / "mql5/Experts/StrategyFactory/SF05_StrategyHost.mq5",
]
errors: list[str] = []
live_authority = re.compile(r"(?<![A-Za-z0-9_])(OrderSend|OrderCheck|CTrade|PositionOpen)\s*\(")
strategy_leak = re.compile(r"\b(NDS|DayeAnatomy|HookAfterF3|TemporalDivergence|ICTAnatomy)\b", re.I)

for path in paths:
    files = [path] if path.is_file() else list(path.rglob("*"))
    for file in files:
        if file.suffix not in {".mqh", ".mq5"}:
            continue
        text = file.read_text(errors="ignore")
        if live_authority.search(text):
            errors.append(f"live authority: {file}")
        if file.parent.name == "Generation" and strategy_leak.search(text):
            errors.append(f"strategy leak: {file}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print("SF05 boundary guard: PASS")
