from __future__ import annotations
import argparse, json
from .conformance import run_conformance

def main(argv=None)->int:
    p=argparse.ArgumentParser(prog="strategy-factory-dataset-v3")
    sub=p.add_subparsers(dest="command",required=True)
    sub.add_parser("conformance")
    args=p.parse_args(argv)
    if args.command=="conformance":
        result=run_conformance(); print(json.dumps(result,indent=2,sort_keys=True)); return 0 if result["accepted"] else 1
    return 2
if __name__=="__main__": raise SystemExit(main())
