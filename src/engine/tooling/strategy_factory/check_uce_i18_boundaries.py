#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
import ast, json
ROOT = find_repository_root(__file__)
PKG = ROOT / "src/engine/packages/strategy_factory_qualification_v3"
errors = []
for path in PKG.glob("*.py"):
    tree = ast.parse(path.read_text(), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            for name in names:
                if name.split(".")[0] in {"socket", "subprocess", "requests", "urllib", "ftplib", "smtplib"}:
                    errors.append(f"external_io_import:{path.name}:{name}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"open", "exec", "eval"}:
            errors.append(f"unsafe_core_call:{path.name}:{node.func.id}")
print(json.dumps({"phase":"UCE-I18","status":"pass" if not errors else "fail","errors":errors},indent=2))
raise SystemExit(1 if errors else 0)
