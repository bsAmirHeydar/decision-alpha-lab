from saed_v4_multimodal_fusion.contracts import FusionConfig

def test_aligned_counts(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_ALIGNED_VIEW_SET.JSON');assert a['domain_view_count']==10 and a['foundation_view_count']==6 and a['common_dim']==16
def test_all_embeddings_fixed_dim(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_ALIGNED_VIEW_SET.JSON');assert all(len(x['embedding'])==16 for x in a['domain_views']+a['foundation_views'])
def test_masks_explicit(load):
 m=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_VIEW_AVAILABILITY_MASK.JSON');assert len(m['items'])==16 and all(set(x)=={'view_name','source_plane','available','quality','age_seconds'} for x in m['items'])
def test_no_external_model_invoked(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_FOUNDATION_VIEW_ENVELOPES.JSON');assert not any(x['external_model_invoked'] for x in a['items'])
def test_known_time_equal(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_15/GOLDEN_ALIGNED_VIEW_SET.JSON');assert a['known_as_of']=='2026-01-05T14:30:01Z' and not a['future_suffix_accessed']
