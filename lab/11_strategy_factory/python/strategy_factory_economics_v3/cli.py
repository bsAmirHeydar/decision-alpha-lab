import argparse,json
from .conformance import run_conformance
def main(argv=None):
    p=argparse.ArgumentParser(prog='strategy-factory-economics-v3'); sub=p.add_subparsers(dest='cmd',required=True); sub.add_parser('conformance'); args=p.parse_args(argv)
    if args.cmd=='conformance':
        r=run_conformance(); print(json.dumps(r,indent=2,sort_keys=True,default=str)); return 0 if r['accepted'] else 1
if __name__=='__main__': raise SystemExit(main())
