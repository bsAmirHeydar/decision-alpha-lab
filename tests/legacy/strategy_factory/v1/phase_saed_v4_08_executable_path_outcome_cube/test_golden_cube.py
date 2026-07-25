from helpers import cube,load
def test_golden_hash_and_exposure():
 c=cube();g=load('releases/history/strategy_factory/artifacts/saed_v4_08/GOLDEN_OUTCOME_CUBE.JSON');assert c.cube_hash==g['cube_hash'];assert c.complete_exposure;assert c.row_count==38
def test_skip_abstain_preserved():
 c=cube();assert c.skip_row_count==1;assert c.abstain_row_count==1
