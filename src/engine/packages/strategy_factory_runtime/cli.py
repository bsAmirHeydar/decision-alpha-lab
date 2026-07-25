from __future__ import annotations
import argparse, json
from pathlib import Path
from .dependency_guard import scan_mql5_boundaries
from .layout import missing_paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", type=Path)
    parser.add_argument("--rules", type=Path,
                        default=Path("src/engine/legacy/strategy_factory/runtime/config/dependency_rules.json"))
    args = parser.parse_args(argv)
    missing = missing_paths(args.repo_root)
    violations = scan_mql5_boundaries(args.repo_root, args.repo_root / args.rules)
    print(json.dumps({
        "missing_paths": missing,
        "boundary_violations": [v.__dict__ for v in violations],
        "ok": not missing and not violations,
    }, indent=2))
    return 0 if not missing and not violations else 1

if __name__ == "__main__":
    raise SystemExit(main())
