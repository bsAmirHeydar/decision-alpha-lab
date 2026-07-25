from __future__ import annotations
import argparse, json
from .conformance import run_conformance


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic UCE-I18 qualification evidence")
    parser.add_argument("--include-synthetic-external-evidence", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run_conformance(args.include_synthetic_external_evidence), indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
