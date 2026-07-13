from strategy_factory_advanced_tasks_v3.golden import ranking_rows
from strategy_factory_advanced_tasks_v3.ranking import *
def test_pairwise_ranking_is_deterministic_and_group_aware():
 rows=ranking_rows();a=PairwiseLinearRanker().fit(rows,('x','g','xg'));b=PairwiseLinearRanker().fit(rows,('x','g','xg'));assert a.state_hash==b.state_hash;report=ranking_metrics(rows,a.predict(rows),3);assert report.group_count==4;assert report.mean_ndcg_at_k>.9;assert report.pairwise_accuracy>.8
