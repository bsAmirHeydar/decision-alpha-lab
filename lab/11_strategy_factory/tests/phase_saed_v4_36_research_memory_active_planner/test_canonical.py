from saed_v4_research_memory_active_planner.canonical import content_hash,semantic_fingerprint,hash_chain,merkle_root

def test_hash_order_invariant(): assert content_hash({'b':2,'a':1})==content_hash({'a':1,'b':2})
def test_semantic_case_invariant(): assert semantic_fingerprint('ABC  x')==semantic_fingerprint('abc x')
def test_chain_deterministic(): assert hash_chain([{'x':1}], 'p')==hash_chain([{'x':1}], 'p')
def test_merkle_order_invariant(): assert merkle_root(['a'*64,'b'*64])==merkle_root(['b'*64,'a'*64])
