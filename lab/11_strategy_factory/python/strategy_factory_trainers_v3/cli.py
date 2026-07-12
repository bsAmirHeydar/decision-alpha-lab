import argparse,json
from dataclasses import asdict
from .conformance import run_conformance
from .registry import TrainerRegistry
from .reference_trainers import register_reference_trainers
def main(argv=None):
 p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True);s.add_parser('conformance');s.add_parser('registry');a=p.parse_args(argv)
 if a.cmd=='conformance':
  r=run_conformance();print(json.dumps(r,indent=2,sort_keys=True));return 0 if r['passed'] else 1
 r=TrainerRegistry();register_reference_trainers(r);print(json.dumps([asdict(x) for x in r.snapshot()],indent=2,sort_keys=True,default=lambda x:x.value));return 0
if __name__=='__main__':raise SystemExit(main())
