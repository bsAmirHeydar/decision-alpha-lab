def test_dataset_shape(load):
 d=load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_CAUSAL_BENCHMARK_DATASET.JSON');assert d['row_count']==240 and d['variable_count']==11 and d['environment_count']==4
def test_dataset_known_time(load):
 d=load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_CAUSAL_BENCHMARK_DATASET.JSON');assert d['known_time_ordered'] and d['future_suffix_access_count']==0
def test_dataset_evidence_roles(load):
 d=load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_CAUSAL_BENCHMARK_DATASET.JSON');assert d['synthetic_only'] and d['protected_evidence_exposures']==0 and not any(r['production_eligible'] for r in d['rows'])
def test_dataset_hashes_present(load):
 d=load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_CAUSAL_BENCHMARK_DATASET.JSON');assert len(d['dataset_hash'])==64 and all(len(r['row_hash'])==64 for r in d['rows'])
def test_environment_balance(load):
 d=load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_CAUSAL_BENCHMARK_DATASET.JSON');counts={e:sum(r['environment_id']==e for r in d['rows']) for e in ['env_0','env_1','env_2','env_3']};assert counts=={e:60 for e in counts}
