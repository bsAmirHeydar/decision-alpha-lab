from __future__ import annotations
import argparse,json
from .conformance import run_conformance
from .registry import validate_registry,registry_hash

def main(argv=None):
    parser=argparse.ArgumentParser();sub=parser.add_subparsers(dest='command',required=True);sub.add_parser('conformance');sub.add_parser('registry')
    args=parser.parse_args(argv)
    if args.command=='conformance':print(json.dumps(run_conformance(),indent=2,sort_keys=True))
    else:validate_registry();print(json.dumps({'registry_hash':registry_hash(),'status':'PASS'},indent=2))
    return 0
if __name__=='__main__':raise SystemExit(main())
