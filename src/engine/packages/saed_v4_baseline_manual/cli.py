from __future__ import annotations
import argparse
from pathlib import Path
from .serialization import load_json,write_json
from .service import build_bundle

def parser():
    p=argparse.ArgumentParser(prog='saed-v4-baseline-manual')
    p.add_argument('--views',required=True);p.add_argument('--hypergraph',required=True);p.add_argument('--lattice',required=True);p.add_argument('--twin',required=True);p.add_argument('--program',action='append',required=True);p.add_argument('--output',required=True)
    return p

def main(argv=None):
    a=parser().parse_args(argv);bundle=build_bundle(load_json(a.views),load_json(a.hypergraph),load_json(a.lattice),load_json(a.twin),[load_json(x) for x in a.program])
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    mapping={'BASELINE_REGISTRY.json':'baseline_registry','BENCHMARK_RESULT.json':'benchmark','EXPOSURE_LEDGER.json':'exposure_ledger','PRETRAINING_CORPUS_MANIFEST.json':'corpus_manifest','INTEGRITY_RECEIPT.json':'integrity_receipt','V4_10_TO_V4_11_HANDOFF.json':'handoff','TELEMETRY.json':'telemetry','CLAIM_LEDGER.json':'claim_ledger'}
    for fn,key in mapping.items():write_json(out/fn,bundle[key])
    for i,p in enumerate(bundle['compiled_programs']):write_json(out/f'COMPILED_PROGRAM_{i+1}.json',p)
    for i,t in enumerate(bundle['decision_traces']):write_json(out/f'DECISION_TRACE_{i+1}.json',t)
    return 0
if __name__=='__main__': raise SystemExit(main())
