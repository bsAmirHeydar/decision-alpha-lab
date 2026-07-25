"""Static Python symbol, import and test-surface scanner."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path
from typing import Iterable

from .classification import critical_domains, owner_domain, probable_production_source
from .io_utils import safe_read_text


def _decorator_name(node: ast.AST) -> str:
    try:
        return ast.unparse(node)
    except Exception:
        return type(node).__name__


def _signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    try:
        return ast.unparse(node.args)
    except Exception:
        return "<unavailable>"


def _module_name(rel_path: str) -> str:
    path = rel_path.removesuffix(".py").removesuffix(".pyi")
    parts = [part for part in path.split("/") if part != "__init__"]
    return ".".join(parts)


def _resolve_import(target: str, module_to_path: dict[str, str]) -> str | None:
    if target in module_to_path:
        return module_to_path[target]
    candidate = target
    while "." in candidate:
        candidate = candidate.rsplit(".", 1)[0]
        if candidate in module_to_path:
            return module_to_path[candidate]
    return None


def scan_python(repo_root: Path, python_paths: Iterable[str]) -> dict[str, list[dict]]:
    paths = sorted(set(python_paths))
    module_to_path = {_module_name(path): path for path in paths}
    symbols: list[dict] = []
    imports: list[dict] = []
    issues: list[dict] = []
    tests: list[dict] = []

    for rel_path in paths:
        path = repo_root / rel_path
        text, read_issue = safe_read_text(path, max_bytes=16 * 1024 * 1024)
        if text is None:
            issues.append({"path": rel_path, "issue": read_issue or "unreadable", "production_candidate": probable_production_source(rel_path)})
            continue
        try:
            tree = ast.parse(text, filename=rel_path, type_comments=True)
        except SyntaxError as exc:
            issues.append({
                "path": rel_path,
                "issue": "syntax_error",
                "message": exc.msg,
                "line": exc.lineno,
                "offset": exc.offset,
                "production_candidate": probable_production_source(rel_path),
            })
            continue
        except Exception as exc:
            issues.append({"path": rel_path, "issue": f"parse_error:{type(exc).__name__}", "production_candidate": probable_production_source(rel_path)})
            continue

        module = _module_name(rel_path)
        parent_stack: list[str] = []
        source_lines = text.splitlines()

        class Visitor(ast.NodeVisitor):
            def _record_symbol(self, node: ast.AST, kind: str, name: str, extra: dict | None = None) -> None:
                qualified = ".".join([module, *parent_stack, name])
                segment = ast.get_source_segment(text, node) or ""
                row = {
                    "path": rel_path,
                    "module": module,
                    "kind": kind,
                    "name": name,
                    "qualified_name": qualified,
                    "line_start": getattr(node, "lineno", None),
                    "line_end": getattr(node, "end_lineno", None),
                    "public": not name.startswith("_"),
                    "owner_domain": owner_domain(rel_path),
                    "critical_domains": critical_domains(rel_path, qualified),
                    "surface_sha256": hashlib.sha256(segment.encode("utf-8")).hexdigest(),
                }
                if extra:
                    row.update(extra)
                symbols.append(row)
                if _is_test_path(rel_path) and kind in {"function", "async_function", "class"} and (name.startswith("test_") or kind == "class" and name.startswith("Test")):
                    tests.append({
                        "path": rel_path,
                        "qualified_name": qualified,
                        "kind": kind,
                        "line": getattr(node, "lineno", None),
                        "critical_domains": critical_domains(rel_path, qualified),
                    })

            def visit_ClassDef(self, node: ast.ClassDef) -> None:
                self._record_symbol(node, "class", node.name, {
                    "bases": [_decorator_name(base) for base in node.bases],
                    "decorators": [_decorator_name(item) for item in node.decorator_list],
                    "docstring_present": bool(ast.get_docstring(node)),
                })
                parent_stack.append(node.name)
                self.generic_visit(node)
                parent_stack.pop()

            def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                self._record_symbol(node, "function", node.name, {
                    "signature": _signature(node),
                    "decorators": [_decorator_name(item) for item in node.decorator_list],
                    "docstring_present": bool(ast.get_docstring(node)),
                })
                parent_stack.append(node.name)
                self.generic_visit(node)
                parent_stack.pop()

            def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
                self._record_symbol(node, "async_function", node.name, {
                    "signature": _signature(node),
                    "decorators": [_decorator_name(item) for item in node.decorator_list],
                    "docstring_present": bool(ast.get_docstring(node)),
                })
                parent_stack.append(node.name)
                self.generic_visit(node)
                parent_stack.pop()

            def visit_Import(self, node: ast.Import) -> None:
                for alias in node.names:
                    target = alias.name
                    imports.append({
                        "source_path": rel_path,
                        "source_module": module,
                        "target_module": target,
                        "resolved_path": _resolve_import(target, module_to_path),
                        "kind": "import",
                        "alias": alias.asname,
                        "line": node.lineno,
                    })

            def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
                target = node.module or ""
                imports.append({
                    "source_path": rel_path,
                    "source_module": module,
                    "target_module": target,
                    "resolved_path": _resolve_import(target, module_to_path) if target else None,
                    "kind": "from_import",
                    "level": node.level,
                    "names": [alias.name for alias in node.names],
                    "line": node.lineno,
                })

        Visitor().visit(tree)

        if not symbols or symbols[-1].get("path") != rel_path:
            # Record module surface even when it contains no classes/functions.
            symbols.append({
                "path": rel_path,
                "module": module,
                "kind": "module",
                "name": module.rsplit(".", 1)[-1] if module else Path(rel_path).stem,
                "qualified_name": module,
                "line_start": 1,
                "line_end": len(source_lines),
                "public": True,
                "owner_domain": owner_domain(rel_path),
                "critical_domains": critical_domains(rel_path, module),
                "surface_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            })

    return {
        "symbols": sorted(symbols, key=lambda x: (x["path"], x.get("line_start") or 0, x["qualified_name"])),
        "imports": sorted(imports, key=lambda x: (x["source_path"], x.get("line") or 0, x.get("target_module") or "")),
        "issues": sorted(issues, key=lambda x: (x["path"], x.get("line") or 0)),
        "tests": sorted(tests, key=lambda x: (x["path"], x.get("line") or 0, x["qualified_name"])),
    }


def _is_test_path(rel_path: str) -> bool:
    lower = rel_path.lower()
    name = Path(rel_path).name.lower()
    return name.startswith("test_") or name.endswith("_test.py") or "/tests/" in f"/{lower}" or lower.startswith("tests/")
