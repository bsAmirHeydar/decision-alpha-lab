from __future__ import annotations
import argparse, json
from dataclasses import asdict
from pathlib import Path
from .io import read_validation_plan
from .folds import compile_walk_forward

def main(argv=None):
    p=argparse.ArgumentParser(prog="strategy-factory-validation")
    sub=p.add_subparsers(dest="command",required=True)
    c=sub.add_parser("compile-folds"); c.add_argument("plan"); c.add_argument("--output",required=True)
    args=p.parse_args(argv)
    if args.command=="compile-folds":
        plan=read_validation_plan(args.plan)
        if not plan.plan_hash: plan=plan.with_hash()
        folds=compile_walk_forward(plan)
        payload=[asdict(x) for x in folds]
        Path(args.output).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        return 0
    return 2
if __name__=="__main__": raise SystemExit(main())
