#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
import ast
import json

ROOT = find_repository_root(__file__)
PKG = ROOT / "src/engine/packages/strategy_factory_operations_v3"
errors: list[str] = []
for path in sorted(PKG.glob("*.py")):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            for name in names:
                if name.split(".")[0] in {"socket", "subprocess", "requests", "urllib", "ftplib", "smtplib", "httpx", "aiohttp"}:
                    errors.append(f"external_io_import:{path.name}:{name}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"open", "exec", "eval", "compile", "__import__"}:
            errors.append(f"unsafe_core_call:{path.name}:{node.func.id}")
        if isinstance(node, ast.Attribute) and node.attr in {"OrderSend", "Buy", "Sell", "WebRequest"}:
            errors.append(f"forbidden_authority_symbol:{path.name}:{node.attr}")
print(json.dumps({"phase":"UCE-I19","status":"pass" if not errors else "fail","python_module_count":len(list(PKG.glob('*.py'))),"errors":errors},indent=2))
raise SystemExit(1 if errors else 0)
