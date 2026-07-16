from pathlib import Path
import argparse,json
from .service import build_reference_bundle

def main(argv=None):
    p=argparse.ArgumentParser(description='Build deterministic SAED V4-14 reference evidence bundle');p.add_argument('--repo-root',default='.');p.add_argument('--out',required=True);a=p.parse_args(argv);r=Path(a.repo_root)
    load=lambda x:json.loads((r/x).read_text(encoding='utf-8'))
    b=build_reference_bundle(load('lab/11_strategy_factory/artifacts/saed_v4_13/V4_13_TO_V4_14_HANDOFF.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_13/GOLDEN_CHECKPOINT_REGISTRY.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_13/GOLDEN_CANDIDATE_EMBEDDINGS.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_13/GOLDEN_COMPILED_MODEL_GRAPH.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_13/GOLDEN_TOURNAMENT.JSON'),load('lab/11_strategy_factory/examples/saed_v4_14/reference_adapter_config.json'),load('lab/11_strategy_factory/examples/saed_v4_14/reference_model_intake_catalog.json'),load('lab/11_strategy_factory/examples/saed_v4_14/reference_candidate_catalog.json'),load('lab/11_strategy_factory/examples/saed_v4_14/reference_pretraining_disclosures.json'),load('lab/11_strategy_factory/examples/saed_v4_14/reference_domain_shift_policy.json'),load('lab/11_strategy_factory/examples/saed_v4_14/reference_compute_exposure_budget.json'))
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(b,indent=2,sort_keys=True)+'
',encoding='utf-8');return 0
if __name__=='__main__':raise SystemExit(main())
