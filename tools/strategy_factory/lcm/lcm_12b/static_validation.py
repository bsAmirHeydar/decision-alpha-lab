from __future__ import annotations
from pathlib import Path

FORBIDDEN = ("OrderSend(", "CTrade", "trade.Buy(", "trade.Sell(", "WebRequest(", "subprocess.Popen(")

def static_validate(root: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(root.rglob("*.py")):
        if path.name == "static_validation.py":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in FORBIDDEN:
            if token in text:
                errors.append(f"FORBIDDEN:{path.name}:{token}")
    return errors
