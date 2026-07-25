import pytest
from dataclasses import replace
from strategy_factory_tournament_v3.golden import golden_run
from strategy_factory_tournament_v3.contracts import *
from strategy_factory_tournament_v3.enums import *
from strategy_factory_tournament_v3.errors import TournamentError
BASE=golden_run()
@pytest.mark.parametrize('field,value',[
 ('row_count',0),('symbols',()),('start_time_ms',13000),('causal_cut_ms',11000),('dataset_hash','bad'),('schema_hash','bad')])
def test_inventory_rejects(field,value):
 inv=BASE[0]
 with pytest.raises(TournamentError):replace(inv,**{field:value})
@pytest.mark.parametrize('field,value',[
 ('event_time_ms',4000),('symbol_scope',()),('context_version','x'),('lifecycle_state','bad value')])
def test_occurrence_rejects(field,value):
 occ=BASE[2][0]
 with pytest.raises(TournamentError):replace(occ,**{field:value})
@pytest.mark.parametrize('field,value',[
 ('declared_at_ms',2000),('locked',False),('treatments',()),('version','v1')])
def test_treatment_freeze_rejects(field,value):
 obj=BASE[3]
 with pytest.raises(TournamentError):replace(obj,**{field:value})
@pytest.mark.parametrize('field,value',[
 ('declared_at_ms',2000),('locked',False),('algorithms',()),('version','v1')])
def test_algorithm_freeze_rejects(field,value):
 obj=BASE[4]
 with pytest.raises(TournamentError):replace(obj,**{field:value})
@pytest.mark.parametrize('field,value',[
 ('max_challengers',-1),('budget_units',0),('seed',-1),('final_test_sealed',False),('metric_ids',()),('critical_gate_ids',())])
def test_tournament_freeze_rejects(field,value):
 obj=BASE[5]
 with pytest.raises(TournamentError):replace(obj,**{field:value})
@pytest.mark.parametrize('field,value',[
 ('minimum_decisions',0),('retraining_allowed',True),('tuning_allowed',True),('start_time_ms',23000),('reconciliation_tolerance',-1)])
def test_paper_plan_rejects(field,value):
 obj=BASE[7]
 with pytest.raises(TournamentError):replace(obj,**{field:value})
