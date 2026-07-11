from __future__ import annotations

import ast
from pathlib import Path

from .models import ContractRecord
from .scope import is_phase00_self_path


def _import_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Import):
        return ",".join(alias.name for alias in node.names)
    if isinstance(node, ast.ImportFrom):
        module = node.module or ""
        names = ",".join(alias.name for alias in node.names)
        return f"{module}:{names}"
    return None


def extract_python_contracts(repo_root: Path) -> list[ContractRecord]:
    records: list[ContractRecord] = []
    for path in sorted(repo_root.rglob("*.py")):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(repo_root).as_posix()
        if is_phase00_self_path(relative):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=relative)
        except SyntaxError:
            continue
        imports = tuple(filter(None, (_import_name(node) for node in tree.body)))
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                public_methods = tuple(
                    child.name
                    for child in node.body
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and not child.name.startswith("_")
                )
                records.append(
                    ContractRecord(
                        path=relative,
                        symbol=node.name,
                        kind="class",
                        public_methods=public_methods,
                        imports=imports,
                        notes="Implicit Python contract; not yet schema-versioned.",
                    )
                )
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
                records.append(
                    ContractRecord(
                        path=relative,
                        symbol=node.name,
                        kind="function",
                        public_methods=(),
                        imports=imports,
                        notes="Module-level callable; contract status requires review.",
                    )
                )
    return records
