from __future__ import annotations
import argparse,json
from .conformance import run_conformance
def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('command',choices=['conformance']);a=p.parse_args(argv)
    print(json.dumps(run_conformance(),sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
