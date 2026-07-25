from saed_v4_sequence_state_space.integrity import build_integrity_receipt
from saed_v4_sequence_state_space.replay import replay_receipt
from saed_v4_sequence_state_space.diff import semantic_diff

def test_integrity_deterministic():
 a=build_integrity_receipt({'b':{'x':1},'a':{'y':2}});b=build_integrity_receipt({'a':{'y':2},'b':{'x':1}});assert a==b
def test_replay_and_diff():
 x={'a':1};assert replay_receipt(x,x)['bit_exact'] and semantic_diff(x,x)['equal']
