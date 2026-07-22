from __future__ import annotations
import ast
from pathlib import Path
FORBIDDEN=("subprocess.Popen", "requests.", "socket.", "OrderSend", "CTrade", "WebRequest")
def static_validate(module_root:Path)->int:
    count=0
    for p in sorted(module_root.glob("*.py")):
        text=p.read_text(encoding="utf-8");ast.parse(text)
        if p.name not in {"service.py", "static_validation.py"} and any(x in text for x in FORBIDDEN): raise ValueError(f"forbidden token in {{p}}")
        count+=1
    return count
