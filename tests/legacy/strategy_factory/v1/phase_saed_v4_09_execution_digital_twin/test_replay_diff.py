import copy
from helpers import built
from saed_v4_execution_twin.replay import replay
from saed_v4_execution_twin.diff import semantic_diff

def test_replay_matches():
    cube,handoff,profile,twin=built();actual,receipt=replay(cube,handoff,profile,twin);assert actual==twin and receipt['matched']

def test_semantic_diff_localizes_change():
    *_,twin=built();other=copy.deepcopy(twin);other['rows'][0]['adjusted_net_r']+=.1;d=semantic_diff(twin,other);assert not d['equivalent'] and d['changed_pairs']
