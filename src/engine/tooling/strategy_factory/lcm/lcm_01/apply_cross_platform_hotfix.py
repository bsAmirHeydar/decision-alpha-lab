from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path


_TARGET_RELATIVE = Path("src/engine/tooling/strategy_factory/lcm/lcm_01/baseline.py")
_IMPORT = "from .cross_platform_integrity import verify_repository_bytes_cross_platform"
_MARKER = "LCM01_CROSS_PLATFORM_INTEGRITY_HOTFIX_V1"
_REPLACEMENT = f'''def verify_repository_bytes(repo_root, root):
    """{_MARKER}: verify frozen bytes while accepting CRLF/LF checkout equivalence."""
    return verify_repository_bytes_cross_platform(repo_root, root)
'''


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _insert_import(source: str) -> str:
    if _IMPORT in source:
        return source

    tree = ast.parse(source)
    insertion_line = 0
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            insertion_line = node.end_lineno or node.lineno
            continue
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            insertion_line = node.end_lineno or node.lineno
            continue
        break

    lines = source.splitlines(keepends=True)
    lines.insert(insertion_line, _IMPORT + "\n")
    return "".join(lines)


def _replace_function(source: str) -> str:
    tree = ast.parse(source)
    matches = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "verify_repository_bytes"
    ]
    if len(matches) != 1:
        raise RuntimeError(
            "expected exactly one top-level verify_repository_bytes function, "
            f"found={len(matches)}"
        )

    node = matches[0]
    if node.end_lineno is None:
        raise RuntimeError("Python AST did not provide end_lineno for verify_repository_bytes")

    lines = source.splitlines(keepends=True)
    start = node.lineno - 1
    end = node.end_lineno
    replacement = _REPLACEMENT
    if end < len(lines) and lines[end].strip():
        replacement += "\n"
    return "".join(lines[:start]) + replacement + "".join(lines[end:])


def apply(repo_root: Path) -> dict[str, object]:
    root = repo_root.resolve()
    target = (root / _TARGET_RELATIVE).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise RuntimeError("hotfix target escaped repository root") from exc
    if not target.is_file():
        raise FileNotFoundError(f"LCM-01 baseline module was not found: {target}")

    before = target.read_bytes()
    source = before.decode("utf-8")
    if _MARKER in source and _IMPORT in source:
        return {
            "applied": False,
            "idempotent": True,
            "target": _TARGET_RELATIVE.as_posix(),
            "sha256": _sha256(before),
        }

    modified = _insert_import(source)
    modified = _replace_function(modified)
    ast.parse(modified)

    encoded = modified.encode("utf-8")
    temporary = target.with_name(target.name + ".lcm01-hotfix.tmp")
    temporary.write_bytes(encoded)
    temporary.replace(target)

    return {
        "applied": True,
        "idempotent": False,
        "target": _TARGET_RELATIVE.as_posix(),
        "before_sha256": _sha256(before),
        "after_sha256": _sha256(encoded),
    }


def main() -> int:
    result = apply(Path.cwd())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
