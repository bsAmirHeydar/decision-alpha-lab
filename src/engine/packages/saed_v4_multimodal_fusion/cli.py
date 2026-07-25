from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
from .service import build_reference_bundle

def main():
    root=find_repository_root(__file__);load=lambda p:json.loads((root/p).read_text())
    b=build_reference_bundle(load('releases/history/strategy_factory/artifacts/saed_v4_14/V4_14_TO_V4_15_HANDOFF.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_14/GOLDEN_CHECKPOINT_REGISTRY.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_14/GOLDEN_ADAPTER_FEATURES.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_14/GOLDEN_TOKEN_SEQUENCE.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_14/GOLDEN_CALIBRATION_REPORT.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_14/GOLDEN_DOMAIN_SHIFT_REPORT.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_14/GOLDEN_TOURNAMENT.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_04/GOLDEN_MULTIMODAL_VIEW_PACKAGE.json'),load('releases/history/strategy_factory/artifacts/saed_v4_04/V4_04_TO_V4_05_HANDOFF.json'),load('examples/legacy/strategy_factory/saed_v4_15/reference_fusion_config.json'),load('examples/legacy/strategy_factory/saed_v4_15/reference_candidate_catalog.json'),load('examples/legacy/strategy_factory/saed_v4_15/reference_support_policy.json'),load('examples/legacy/strategy_factory/saed_v4_15/reference_missingness_policy.json'),load('examples/legacy/strategy_factory/saed_v4_15/reference_compute_exposure_budget.json'))
    print(json.dumps({'phase':'SAED_V4_15','bundle_hash':b['bundle_hash'],'reference_champion_id':b['tournament']['reference_champion_id'],'handoff_hash':b['handoff']['handoff_hash']},indent=2))
if __name__=='__main__':main()
