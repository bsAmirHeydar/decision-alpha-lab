from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path


def probe(repo: Path) -> dict:
    repo = repo.resolve()
    for relative in ("src/engine/packages", "src/engine/legacy/core", "src/engine/legacy/infrastructure/utils"):
        path = repo / relative
        if path.is_dir() and str(path) not in sys.path:
            sys.path.insert(0, str(path))
    modules = [
        "strategy_factory_context",
        "strategy_factory_statistics",
        "strategy_factory_validation",
    ]
    modules.append(
        "tools.strategy_factory"
        if (repo / "tools/strategy_factory/__init__.py").is_file()
        else "src.engine.tooling.strategy_factory"
    )
    results = []
    for module in modules:
        try:
            imported = importlib.import_module(module)
            results.append({"module": module, "status": "PASS", "file": str(getattr(imported, "__file__", ""))})
        except Exception as exc:
            results.append({"module": module, "status": "FAIL", "error": f"{type(exc).__name__}: {exc}"})
    mql5_count = sum(1 for root in (repo / "mql5",) if root.exists() for path in root.rglob("*") if path.suffix.lower() in {".mq5", ".mqh"})
    result = {
        "status": "PASS" if all(row["status"] == "PASS" for row in results) and mql5_count > 0 else "FAIL",
        "modules": results,
        "mql5_source_count": mql5_count,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    result = probe(Path(args.repo_root))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
