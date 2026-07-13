import argparse,json
from dataclasses import asdict
from .conformance import run_conformance
from .registry import ClassicalAlgorithmRegistry
def default(x):return x.value if hasattr(x,'value') else str(x)
def main(argv=None):
 p=argparse.ArgumentParser(prog='strategy-factory-classical-v3');s=p.add_subparsers(dest='cmd',required=True);s.add_parser('conformance');s.add_parser('catalog');a=p.parse_args(argv)
 if a.cmd=='conformance':
  o=run_conformance();print(json.dumps(o,indent=2,sort_keys=True,default=default));return 0 if o['passed'] else 1
 o=ClassicalAlgorithmRegistry().freeze().snapshot();print(json.dumps(asdict(o),indent=2,sort_keys=True,default=default));return 0
if __name__=='__main__':raise SystemExit(main())
