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
    "os.remove",
    "shutil.rmtree",
)

ALLOWED_DELETE_MODULES = {"recovery.py"}


def static_validate(module_root: Path) -> int:
    count = 0
    for path in sorted(module_root.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        ast.parse(text)
        if path.name == "static_validation.py":
            count += 1
            continue
        forbidden = []
        for token in FORBIDDEN:
            if token in text and not (path.name in ALLOWED_DELETE_MODULES and token == "shutil.rmtree"):
                forbidden.append(token)
        if forbidden:
            raise ValueError(f"forbidden capability token in {path}: {forbidden}")
        count += 1
    if count < 12:
        raise ValueError("incomplete LCM-16B module set")
    return count
