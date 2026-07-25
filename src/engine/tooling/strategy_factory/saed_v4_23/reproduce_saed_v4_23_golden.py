from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from saed_v4_offline_policy_research.service import run
load=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
ex=ROOT/'examples/legacy/strategy_factory/saed_v4_23';art=ROOT/'releases/history/strategy_factory/artifacts/saed_v4_23'
out=run(load(ex/'FULL_REFERENCE_CONFIG.JSON'),load(ex/'UPSTREAM_V4_22_DOCUMENTS.JSON'),load(ex/'LOGGED_TRAJECTORIES.JSON'),load(ex/'MANUAL_BASELINE_POLICY.JSON'))
checks={'GOLDEN_UPSTREAM_RECEIPT':out['upstream_receipt'],'GOLDEN_DATASET_SUMMARY':out['dataset_summary'],'GOLDEN_REWARD_AUDIT':out['reward_audit'],'GOLDEN_BEHAVIOR_POLICY':out['behavior_policy'],'GOLDEN_ACTION_MASK_REPORT':out['action_mask_report'],'GOLDEN_POLICY_CHALLENGE_MATRIX':out['challenge_matrix'],'GOLDEN_BASELINE_PRESERVATION':out['baseline_preservation'],'GOLDEN_TRIAL_LEDGER':out['trial_ledger'],'GOLDEN_EXPOSURE_LEDGER':out['exposure_ledger'],'GOLDEN_BUDGET_SNAPSHOT':out['budget_snapshot'],'GOLDEN_OFFLINE_POLICY_RESEARCH_CERTIFICATE':out['certificate'],'GOLDEN_REPLAY_RECEIPT':out['replay_receipt'],'V4_23_TO_V4_24_HANDOFF':out['handoff']}
for name,value in checks.items():assert value==load(art/f'{name}.JSON'),name
print(f'V4-23 golden reproduction passed: {len(checks)} exact artifacts; replay {out["replay_receipt"]["replay_hash"]}')
