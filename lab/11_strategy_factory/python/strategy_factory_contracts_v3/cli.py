"""Command-line utilities for contract conformance and vector generation."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .fixtures import build_cross_language_vectors


def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(prog="strategy-factory-contracts-v3")
    sub=parser.add_subparsers(dest="command",required=True)
    vector=sub.add_parser("generate-vectors")
    vector.add_argument("output",type=Path)
    check=sub.add_parser("check-vector-file")
    check.add_argument("path",type=Path)
    args=parser.parse_args(argv)
    expected=build_cross_language_vectors()
    if args.command=="generate-vectors":
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(expected,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        return 0
    actual=json.loads(args.path.read_text(encoding="utf-8"))
    if actual!=expected:raise SystemExit("vector file diverges from implementation")
    print("UCEE-I01 vectors: PASS")
    return 0

if __name__=="__main__":raise SystemExit(main())
