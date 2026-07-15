import copy,pytest
from saed_v4_self_supervised_pretraining.models import TrainingConfig
from saed_v4_self_supervised_pretraining.budget import build_compute_budget,assert_budget
from saed_v4_self_supervised_pretraining.errors import BudgetError

def test_budget_accepts_config(config):
 c=TrainingConfig.from_mapping(config);b=build_compute_budget(1200,6,12);assert_budget(c,b)
def test_pair_budget_rejected(config):
 c=TrainingConfig.from_mapping(config);b=build_compute_budget(10,6,12)
 with pytest.raises(BudgetError):assert_budget(c,b)
def test_dimension_budget_rejected(config):
 c=TrainingConfig.from_mapping(config);b=build_compute_budget(1200,6,8)
 with pytest.raises(BudgetError):assert_budget(c,b)
def test_network_denied():assert not build_compute_budget(10,1,4)['external_network_allowed']
