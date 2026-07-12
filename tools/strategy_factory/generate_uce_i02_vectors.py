#!/usr/bin/env python3
"""Regenerate deterministic UCE-I02 reference conformance reports."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path

def main()->int:
    parser=argparse.ArgumentParser();parser.add_argument("root",nargs="?",default=".");args=parser.parse_args();root=Path(args.root).resolve();sys.path.insert(0,str(root/"lab/11_strategy_factory/python"))
    from strategy_factory_contexts_v3 import SyntheticBreakContextPackage,EXP0017ContextPackage,ContextConformanceHarness
    from strategy_factory_contexts_v3.fixtures import synthetic_records,synthetic_future_mutations,exp0017_records
    out=root/"lab/11_strategy_factory/examples/uce_i02";out.mkdir(parents=True,exist_ok=True)
    for name,p,rows,mut in (("synthetic",SyntheticBreakContextPackage(),synthetic_records(),synthetic_future_mutations()),("exp0017",EXP0017ContextPackage(),exp0017_records(),[])):
        report=ContextConformanceHarness().run(p,rows,mut)
        (out/f"{name}_conformance_report.golden.json").write_text(json.dumps(report.material(),indent=2,sort_keys=True,default=str)+"\n",encoding="utf-8")
        if not report.passed: return 1
    print("UCE-I02 vectors regenerated");return 0
if __name__=="__main__": raise SystemExit(main())
