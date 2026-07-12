"""Command-line utilities for package linting and reference conformance."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from .reference import SyntheticBreakContextPackage, EXP0017ContextPackage
from .fixtures import synthetic_records, synthetic_future_mutations, exp0017_records
from .conformance import ContextConformanceHarness, ContextPackageLinter

def _package(name:str): return SyntheticBreakContextPackage() if name=="synthetic" else EXP0017ContextPackage()
def main(argv=None)->int:
    parser=argparse.ArgumentParser(prog="strategy-factory-contexts-v3")
    sub=parser.add_subparsers(dest="command",required=True)
    lint=sub.add_parser("lint-reference"); lint.add_argument("package",choices=("synthetic","exp0017"))
    run=sub.add_parser("run-reference-conformance"); run.add_argument("package",choices=("synthetic","exp0017")); run.add_argument("--output")
    args=parser.parse_args(argv); package=_package(args.package)
    if args.command=="lint-reference":
        findings=ContextPackageLinter().lint(package); print(json.dumps([{"code":x.code,"severity":x.severity.value,"message":x.message,"evidence":dict(x.evidence)} for x in findings],indent=2,sort_keys=True)); return 1 if any(x.severity.value in ("error","fatal") for x in findings) else 0
    records=synthetic_records() if args.package=="synthetic" else exp0017_records(); mutations=synthetic_future_mutations() if args.package=="synthetic" else []
    report=ContextConformanceHarness().run(package,records,mutations); text=json.dumps(report.material(),indent=2,sort_keys=True)
    if args.output: Path(args.output).write_text(text+"\n",encoding="utf-8")
    else: print(text)
    return 0 if report.passed else 1
if __name__=="__main__": raise SystemExit(main())
