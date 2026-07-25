from strategy_factory_advanced_tasks_v3.multitask import SharedLinearHeads,RegimeGate
from strategy_factory_trainers_v3.contracts import TrainingRow
from strategy_factory_trainers_v3.enums import SplitRole

def rows():return tuple(TrainingRow(f'r{i}',(float(i),float(i%2)),(float(i),float(i%2)),SplitRole.TRAIN,'f','c',i,i) for i in range(20))
def test_shared_heads_and_sparse_regime_fallback():
 rs=rows();m=SharedLinearHeads(('utility','risk')).fit(rs);assert m.report(rs).weighted_loss>=0;g=RegimeGate(20).fit(rs,{r.row_id:('a' if int(r.features[0])<10 else 'b') for r in rs},{'a':'expert_a','b':'expert_b'},'global');assert g.select(rs[0]).global_model_used
