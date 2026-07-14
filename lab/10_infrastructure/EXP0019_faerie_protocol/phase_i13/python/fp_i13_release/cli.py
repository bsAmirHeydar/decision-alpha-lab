from __future__ import annotations
import argparse,json
from .conformance import run_conformance
from .profiles import PROFILES

def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('command',choices=['conformance','profiles']);a=p.parse_args(argv)
    if a.command=='conformance': print(json.dumps(run_conformance(),indent=2,sort_keys=True))
    else: print(json.dumps([{'profile_id':x.profile_id.value,'profile_hash':x.profile_hash} for x in PROFILES],indent=2))
    return 0
if __name__=='__main__': raise SystemExit(main())
