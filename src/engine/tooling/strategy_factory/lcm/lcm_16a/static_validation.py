from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN = (
    "subprocess.Popen",
    "requests.",
    "socket.",
    "OrderSend",
    "CTrade",
    "WebRequest",
    ".unlink(",
    "rmtree(",
    "os.remove",
    "shutil.rmtree",
)


def static_validate(module_root: Path) -> int:
    count = 0
    for path in sorted(module_root.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        ast.parse(text)
        if path.name not in {"static_validation.py"}:
            forbidden = [token for token in FORBIDDEN if token in text]
            if forbidden:
                raise ValueError(f"forbidden capability token in {path}: {forbidden}")
        count += 1
    if count < 10:
        raise ValueError("incomplete LCM-16A module set")
    return count
