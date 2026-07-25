from __future__ import annotations
from pathlib import Path
FORBIDDEN=("Order"+"Send(","Order"+"SendAsync(","C"+"Trade","trade."+"Buy(","trade."+"Sell(")

def validate_module(module_root:Path):
    errors=[]
    for path in module_root.rglob("*.py"):
        text=path.read_text(encoding="utf-8")
        for token in FORBIDDEN:
            if token in text:errors.append(f"FORBIDDEN_AUTHORITY_TOKEN:{path}:{token}")
    return errors
