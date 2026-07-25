import pytest
from strategy_factory_trainers_v3 import *
from strategy_factory_trainers_v3.golden import build_case
def test_cancelled_budget():
 s,rows,p=build_case(TaskKind.REGRESSION);t=CancellationToken();t.cancel('test')
 with pytest.raises(ResourceBudgetError):BudgetGuard(p.resources,s,t).start()
def test_model_card_and_manifest():
 r=TrainerRegistry();register_reference_trainers(r);s,rows,p=build_case(TaskKind.REGRESSION);x=TaskOrchestrator(r).run(p,s,rows,'abc');assert x.artifact_manifest.code_hash=='abc';assert 'Ungoverned live trading' in x.model_card.prohibited_uses
