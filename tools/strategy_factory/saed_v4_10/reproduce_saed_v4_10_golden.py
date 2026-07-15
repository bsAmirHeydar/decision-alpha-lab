from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_baseline_manual.serialization import load_json,write_json
from saed_v4_baseline_manual.service import build_bundle

def main():
 v=load_json(ROOT/'lab/11_strategy_factory/artifacts/saed_v4_04/GOLDEN_MULTIMODAL_VIEW_PACKAGE.json');h=load_json(ROOT/'lab/11_strategy_factory/artifacts/saed_v4_05/GOLDEN_SEMANTIC_TEMPORAL_HYPERGRAPH.json');l=load_json(ROOT/'lab/11_strategy_factory/artifacts/saed_v4_07/GOLDEN_ACTION_LATTICE.JSON');t=load_json(ROOT/'lab/11_strategy_factory/artifacts/saed_v4_09/GOLDEN_EXECUTION_TWIN.JSON');ps=[load_json(ROOT/'lab/11_strategy_factory/examples/saed_v4_10/manual_doctrine_reference_v1.json'),load_json(ROOT/'lab/11_strategy_factory/examples/saed_v4_10/manual_conservative_reference_v1.json')];b=build_bundle(v,h,l,t,ps);out=ROOT/'lab/11_strategy_factory/artifacts/saed_v4_10_reproduced';out.mkdir(parents=True,exist_ok=True);write_json(out/'GOLDEN_BASELINE_REGISTRY.JSON',b['baseline_registry']);write_json(out/'GOLDEN_BENCHMARK_RESULT.JSON',b['benchmark']);write_json(out/'GOLDEN_PRETRAINING_CORPUS_MANIFEST.JSON',b['corpus_manifest']);write_json(out/'V4_10_TO_V4_11_HANDOFF.JSON',b['handoff']);return 0
if __name__=='__main__':raise SystemExit(main())
