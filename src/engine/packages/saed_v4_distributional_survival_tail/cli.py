from tools.repository_paths import find_repository_root
from pathlib import Path
import json
from .service import build_reference_bundle
ROOT=find_repository_root(__file__)
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def main():
    b=build_reference_bundle(load('releases/history/strategy_factory/artifacts/saed_v4_15/V4_15_TO_V4_16_HANDOFF.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_CHECKPOINT_REGISTRY.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_FUSION_OUTPUTS.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_ALIGNED_VIEW_SET.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_INTEGRITY_RECEIPT.JSON'),load('examples/legacy/strategy_factory/saed_v4_16/reference_event_definition_registry.json'),load('examples/legacy/strategy_factory/saed_v4_16/reference_censoring_policy.json'),load('examples/legacy/strategy_factory/saed_v4_16/reference_dataset_spec.json'),load('examples/legacy/strategy_factory/saed_v4_16/reference_model_config.json'),load('examples/legacy/strategy_factory/saed_v4_16/reference_candidate_catalog.json'),load('examples/legacy/strategy_factory/saed_v4_16/reference_tail_policy.json'),load('examples/legacy/strategy_factory/saed_v4_16/reference_compute_exposure_budget.json'))
    print(json.dumps({'phase':'SAED_V4_16','version':'1.0.0','dataset_hash':b['survival_dataset']['dataset_hash'],'reference_champion_id':b['tournament']['reference_champion_id'],'registry_hash':b['checkpoint_registry']['registry_hash'],'handoff_hash':b['handoff']['handoff_hash'],'production_authority':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
