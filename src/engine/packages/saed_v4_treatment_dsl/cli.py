from __future__ import annotations

import argparse
import json
from pathlib import Path

from .catalog import institutional_capability_profile, institutional_policy, institutional_registry
from .contracts import load_json
from .parser import parse_program
from .serialization import write_json
from .service import TreatmentDslService


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="saed-v4-treatment-dsl")
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build", help="Build a deterministic V4-06 finite DSL package")
    build.add_argument("--graph", required=True)
    build.add_argument("--handoff", required=True)
    build.add_argument("--program", action="append", required=True)
    build.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    if args.command == "build":
        graph = load_json(args.graph)
        handoff = load_json(args.handoff)
        programs = tuple(parse_program(load_json(path)) for path in args.program)
        package = TreatmentDslService().build_package(
            graph=graph,
            handoff=handoff,
            registry=institutional_registry(),
            policy=institutional_policy(),
            capability_profile=institutional_capability_profile(),
            sources=programs,
        )
        write_json(args.output, package)
        print(json.dumps({"package_id": package.package_id, "package_hash": package.package_hash, "program_count": len(package.programs)}, sort_keys=True))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
