def test_dataset_shape(load):
 d=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_SURVIVAL_DATASET.JSON');assert d['row_count']==240 and d['feature_dim']==16 and d['split_counts']=={'train':144,'calibration':48,'selection_validation':48}
def test_dataset_chronological(load):
 d=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_SURVIVAL_DATASET.JSON');assert d['known_time_ordered'] and d['chronological_split'] and d['synthetic_only']
def test_frozen_feature_lineage(load):
 d=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_SURVIVAL_DATASET.JSON');h=load('lab/11_strategy_factory/artifacts/saed_v4_15/V4_15_TO_V4_16_HANDOFF.JSON');assert all(r['source_registry_hash']==h['fusion_checkpoint_registry_hash'] for r in d['rows']) and all(len(r['features'])==16 for r in d['rows'])
def test_no_future_suffix(load):
 d=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_SURVIVAL_DATASET.JSON');assert not any(r['future_suffix_accessed'] for r in d['rows'])
def test_no_production_eligibility(load):
 d=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_SURVIVAL_DATASET.JSON');assert not any(r['production_eligible'] for r in d['rows'])
def test_heavy_tail_present(load):
 d=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_SURVIVAL_DATASET.JSON');v=[r['net_r'] for r in d['rows'] if r['outcome_observed']];assert min(v)<-2 and max(v)>2
