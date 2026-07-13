"""Command-line entry point for UCE-I10 conformance and catalog inspection."""

from __future__ import annotations

import argparse
import json

from .conformance import run_conformance


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="strategy-factory-deep-views-v3")
    parser.add_argument("command", choices=("conformance", "catalog"))
    arguments = parser.parse_args(argv)
    if arguments.command == "conformance":
        output = run_conformance()
    else:
        from .catalog import CATALOG

        output = {
            "release": "UCE-I10",
            "count": len(CATALOG),
            "algorithms": [
                {
                    "key": descriptor.key,
                    "family": descriptor.family.value,
                    "native": descriptor.native,
                    "determinism": descriptor.determinism,
                    "dependency_profile": descriptor.dependency_profile,
                    "export_paths": [path.value for path in descriptor.export_paths],
                }
                for descriptor in CATALOG
            ],
        }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if output.get("passed", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
