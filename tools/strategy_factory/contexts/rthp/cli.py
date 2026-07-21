from __future__ import annotations

import argparse
import json
from pathlib import Path

from .compiler import compile_package
from .fixtures import validate_fixtures
from .patch_verify import verify
from .validation import validate_package


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    command = sub.add_parser("validate-package")
    command.add_argument("--package-root", required=True)

    command = sub.add_parser("validate-fixtures")
    command.add_argument("--package-root", required=True)

    command = sub.add_parser("compile")
    command.add_argument("--package-root", required=True)
    command.add_argument("--output", required=True)

    command = sub.add_parser("verify-patch")
    command.add_argument("--repo-root", required=True)
    command.add_argument("--hash-ledger", required=True)

    args = parser.parse_args(argv)

    if args.cmd == "validate-package":
        result = validate_package(Path(args.package_root))
    elif args.cmd == "validate-fixtures":
        result = validate_fixtures(Path(args.package_root))
    elif args.cmd == "verify-patch":
        result = verify(Path(args.repo_root), Path(args.hash_ledger))
    else:
        compiled = compile_package(Path(args.package_root))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(compiled, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        result = {"passed": True, "compiled_digest": compiled["compiled_digest"]}

    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if result.get("passed", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
