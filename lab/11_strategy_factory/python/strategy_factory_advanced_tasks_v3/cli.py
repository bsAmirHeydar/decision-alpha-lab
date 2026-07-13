import argparse,json
from dataclasses import asdict
from .conformance import run_conformance
from .registry import AdvancedTaskRegistry

def main(argv=None):
 p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True);s.add_parser('conformance');s.add_parser('registry');a=p.parse_args(argv)
 if a.cmd=='conformance':
  r=run_conformance();print(json.dumps(r,indent=2,sort_keys=True,default=str));return 0 if r['passed'] else 1
 snap=AdvancedTaskRegistry().freeze().snapshot();print(json.dumps(asdict(snap),indent=2,sort_keys=True,default=lambda x:x.value));return 0
if __name__=='__main__':raise SystemExit(main())
