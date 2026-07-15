from __future__ import annotations
import argparse
from pathlib import Path
from .service import build_from_files
from .serialization import dumps

def main(argv=None):
    p=argparse.ArgumentParser(prog='saed-v4-outcome-cube');sub=p.add_subparsers(dest='command',required=True);b=sub.add_parser('build')
    for name in ('lattice','handoff','context','path','policy','cost_registry','output'):b.add_argument('--'+name.replace('_','-'),required=True)
    b.add_argument('--cost-model-id',required=True);b.add_argument('--cost-model-version',required=True)
    a=p.parse_args(argv)
    cube=build_from_files(a.lattice,a.handoff,a.context,a.path,a.policy,a.cost_registry,a.cost_model_id,a.cost_model_version);Path(a.output).write_text(dumps(cube),encoding='utf-8');print(cube.cube_hash);return 0
if __name__=='__main__':raise SystemExit(main())
