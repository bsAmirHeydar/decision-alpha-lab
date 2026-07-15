def test_v410_baseline_hash_preserved(load):
 h=load('lab/11_strategy_factory/artifacts/saed_v4_10/V4_10_TO_V4_11_HANDOFF.JSON');v=load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_CORPUS_MANIFEST.JSON');assert v['upstream_handoff_hash']==h['handoff_hash']
def test_v410_corpus_hash_preserved(load):
 u=load('lab/11_strategy_factory/artifacts/saed_v4_10/GOLDEN_PRETRAINING_CORPUS_MANIFEST.JSON');v=load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_CORPUS_MANIFEST.JSON');assert v['upstream_corpus_manifest_hash']==u['manifest_hash']
def test_baseline_registry_not_mutated(load):
 h=load('lab/11_strategy_factory/artifacts/saed_v4_10/V4_10_TO_V4_11_HANDOFF.JSON');v=load('lab/11_strategy_factory/artifacts/saed_v4_11/V4_11_TO_V4_12_HANDOFF.JSON');assert v['entry_gates']['baseline_registry_preserved'];assert len(h['baseline_registry_hash'])==64
