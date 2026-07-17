import pytest
from saed_v4_model_risk_supply_chain.canonical import content_hash,hash_chain,stable_id

def test_hash_key_order_invariant():assert content_hash({'b':2,'a':1})==content_hash({'a':1,'b':2})
def test_stable_id_prefix():assert stable_id('x',{'a':1}).startswith('x_')
def test_hash_chain_links():
    c=hash_chain([{'x':1},{'x':2},{'x':3}],'e');assert c[0]['previous_hash']=='0'*64;assert c[1]['previous_hash']==c[0]['event_hash'];assert c[2]['previous_hash']==c[1]['event_hash']
@pytest.mark.parametrize('n',range(20))
def test_hash_determinism_parametric(n):assert content_hash({'n':n})==content_hash({'n':n})
