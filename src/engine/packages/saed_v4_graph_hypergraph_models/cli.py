from pathlib import Path
import argparse,json
from .service import build_reference_bundle
def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--repo-root',default='.');p.add_argument('--out',required=True);a=p.parse_args(argv);r=Path(a.repo_root)
    load=lambda x:json.loads((r/x).read_text(encoding='utf-8'))
    b=build_reference_bundle(load('releases/history/strategy_factory/artifacts/saed_v4_05/GOLDEN_SEMANTIC_TEMPORAL_HYPERGRAPH.json'),load('releases/history/strategy_factory/artifacts/saed_v4_05/GOLDEN_GRAPH_INTEGRITY_RECEIPT.json'),load('releases/history/strategy_factory/artifacts/saed_v4_12/V4_12_TO_V4_13_HANDOFF.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_12/GOLDEN_CHECKPOINT_REGISTRY.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_12/GOLDEN_DISTILLATION.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_12/GOLDEN_STATE_SNAPSHOTS.JSON'),load('examples/legacy/strategy_factory/saed_v4_13/reference_graph_spec.json'),load('examples/legacy/strategy_factory/saed_v4_13/reference_candidate_catalog.json'),load('examples/legacy/strategy_factory/saed_v4_13/reference_objective_catalog.json'),load('examples/legacy/strategy_factory/saed_v4_13/reference_compute_envelope.json'))
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(b,indent=2,sort_keys=True)+'\n');return 0
if __name__=='__main__':raise SystemExit(main())
