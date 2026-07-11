from __future__ import annotations
import argparse, json
from pathlib import Path
from .examples import reference_governance_bundle
from .reports import write_governance_bundle

def main(argv=None):
    parser=argparse.ArgumentParser(prog="strategy-factory-governance")
    sub=parser.add_subparsers(dest="command",required=True)
    ref=sub.add_parser("emit-reference",help="emit the deterministic Phase 14 reference governance bundle")
    ref.add_argument("output",type=Path)
    args=parser.parse_args(argv)
    if args.command=="emit-reference":
        _,evidence,_,evaluation,registry,_,snapshot,release,report=reference_governance_bundle()
        write_governance_bundle(args.output,evidence=evidence,evaluation=evaluation,
            registry=registry,snapshot=snapshot,release_manifest=release,report_manifest=report)
        print(json.dumps({"snapshot_hash":snapshot.snapshot_hash,"release_hash":release.release_hash,
                          "decision_chain_hash":registry.ledger.chain_hash},sort_keys=True))
        return 0
    return 2

if __name__=="__main__":raise SystemExit(main())
