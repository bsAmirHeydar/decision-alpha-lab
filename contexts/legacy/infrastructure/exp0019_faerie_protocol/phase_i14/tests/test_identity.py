from fp_i14_diagnostic import *
def test_event_id_product_independent(manifests,facts):
    es=[adapt_fact(p,manifests[p],facts[0]) for p in ProductKind];assert len({e.computed_event_id for e in es})==1
def test_event_hash_product_specific(manifests,facts):
    es=[adapt_fact(p,manifests[p],facts[0]) for p in ProductKind];assert len({e.event_hash for e in es})==3
def test_semantic_hash_product_independent(manifests,facts):
    es=[adapt_fact(p,manifests[p],facts[0]) for p in ProductKind];assert len({e.semantic_hash for e in es})==1
def test_payload_change_changes_semantic_hash(manifests,facts):
    m=manifests[ProductKind.INDICATOR];a=adapt_fact(m.product,m,facts[0]);b=adapt_fact(m.product,m,SemanticFact(1,facts[0].event_time_utc_ms,facts[0].event_type,facts[0].semantic_id,{'changed':1}));assert a.semantic_hash!=b.semantic_hash
