"""Minimal offline CLI for registry, vectors and golden gate diagnostics."""
from __future__ import annotations
import argparse,json
from dataclasses import asdict
from .canonical import canonical_value
from .conformance import generate_vectors
from .golden import golden_family_definition,golden_universe
from .multiplicity import multiplicity_report
from .registry import registry_snapshot

def main(argv=None)->int:
    parser=argparse.ArgumentParser(prog="strategy-factory-promotion-v3")
    parser.add_argument("command",choices=("registry","vectors","golden-multiplicity")); args=parser.parse_args(argv)
    if args.command=="registry": payload=registry_snapshot()
    elif args.command=="vectors": payload=generate_vectors()
    else: payload=asdict(multiplicity_report(golden_universe(),golden_family_definition()))
    print(json.dumps(canonical_value(payload),indent=2,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
