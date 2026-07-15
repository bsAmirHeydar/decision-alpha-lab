from helpers import cube
from saed_v4_outcome_cube.diff import semantic_diff
def test_self_diff_empty():
 c=cube();d=semantic_diff(c,c);assert d['changed_count']==0 and d['ranking_semantics']=='none'
