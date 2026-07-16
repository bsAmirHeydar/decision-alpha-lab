def test_candidate_count(load):assert load('lab/11_strategy_factory/artifacts/saed_v4_17/GOLDEN_CANDIDATE_METRICS.JSON')['row_count']==5
def test_baseline_preserved(load):assert load('lab/11_strategy_factory/artifacts/saed_v4_17/GOLDEN_TOURNAMENT.JSON')['baseline_preserved']
def test_champion_research_only(load):
 x=load('lab/11_strategy_factory/artifacts/saed_v4_17/GOLDEN_TOURNAMENT.JSON');assert x['champion_is_research_only'] and not x['production_authority'] and not x['causal_claim_authority']
def test_registry_immutable(load):
 x=load('lab/11_strategy_factory/artifacts/saed_v4_17/GOLDEN_CHECKPOINT_REGISTRY.JSON');assert x['immutable'] and not x['causal_claim_authority'] and not x['runtime_authority'] and not x['production_authority']
def test_all_checkpoints_nonproduction(load):
 x=load('lab/11_strategy_factory/artifacts/saed_v4_17/GOLDEN_CANDIDATE_CHECKPOINTS.JSON');assert all(not r['production_eligible'] and not r['runtime_eligible'] and not r['causal_claim_eligible'] for r in x['items'])
