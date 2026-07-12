from __future__ import annotations
import argparse,json
from .conformance import run_conformance
from .golden import run_golden_paths
def main(argv=None):
    p=argparse.ArgumentParser(prog='strategy-factory-treatment-compiler-v3'); sub=p.add_subparsers(dest='cmd',required=True)
    sub.add_parser('conformance'); sub.add_parser('golden-paths')
    a=p.parse_args(argv)
    data=run_conformance() if a.cmd=='conformance' else {'treatment':run_golden_paths()[0],'paths':run_golden_paths()[1]}
    print(json.dumps(data,indent=2,sort_keys=True,default=str)); return 0 if data.get('passed',True) else 1
if __name__=='__main__': raise SystemExit(main())
