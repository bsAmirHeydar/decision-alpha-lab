from __future__ import annotations
import argparse
import json
from pathlib import Path
from .service import run


def main(argv=None):
    parser = argparse.ArgumentParser(prog="saed-v4-29-hidden-evaluation-air-gap")
    for name in ["config", "upstream", "custody_manifest", "candidate", "sealed_fixture", "output"]:
        parser.add_argument(f"--{name.replace('_', '-')}", required=True)
    args = parser.parse_args(argv)

    def load(path: str):
        return json.loads(Path(path).read_text(encoding="utf-8"))

    result = run(
        load(args.config),
        load(args.upstream),
        load(args.custody_manifest),
        load(args.candidate),
        load(args.sealed_fixture),
    )
    Path(args.output).write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
