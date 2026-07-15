from __future__ import annotations
import argparse,json
from pathlib import Path
from .serialization import load_json,dump_json
from .service import ActionLatticeService

def main(argv=None)->int:
    p=argparse.ArgumentParser(prog='saed-v4-action-lattice');sub=p.add_subparsers(dest='command',required=True)
    s=sub.add_parser('solve');
    for name in ('package','handoff','policy','domains','request'):s.add_argument(f'--{name}',required=True)
    s.add_argument('--output',required=True)
    a=p.parse_args(argv)
    if a.command=='solve':
        out=ActionLatticeService().solve(package=load_json(a.package),handoff=load_json(a.handoff),policy_document=load_json(a.policy),domain_registry=load_json(a.domains),request=load_json(a.request));dump_json(a.output,out);return 0
    return 2
if __name__=='__main__':raise SystemExit(main())
