from strategy_factory_training.examples import build_reference_training_bundle
from strategy_factory_training import *

def test_ranking_pairs_have_stable_identity():
    rows=rows_for_role(build_reference_training_bundle()[0].rows,DatasetRole.TRAIN)
    a=build_ranking_pairs(rows);b=build_ranking_pairs(rows);assert [p.pair_id for p in a]==[p.pair_id for p in b] and len(a)>0
    scores={r.row_id:float(r.label_value) for r in rows};assert pairwise_accuracy(a,scores)==1.0
