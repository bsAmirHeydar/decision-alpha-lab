from strategy_factory_advanced_tasks_v3.registry import AdvancedTaskRegistry
from strategy_factory_advanced_tasks_v3.trainer_plugins import register_advanced_trainers
from strategy_factory_trainers_v3.registry import TrainerRegistry

def test_exact_registry_and_trainer_registration():
 s=AdvancedTaskRegistry().freeze().snapshot();assert len(s.descriptors)==18;assert s.frozen;r=TrainerRegistry();keys=register_advanced_trainers(r);assert len(keys)==5;assert r.resolve_exact('uce.advanced.pairwise_linear_ranker','1.0.0')
