from strategy_factory_dataset_v3.golden import *
from strategy_factory_dataset_v3.cube import CounterfactualOutcomeCubeBuilder
from strategy_factory_dataset_v3.labels import LabelCompiler
from strategy_factory_dataset_v3.enums import TaskKind

def _cube():
 a=golden_anchors(1)[0]; return CounterfactualOutcomeCubeBuilder().build(a,golden_treatments(a),golden_path(a),golden_scenarios(),[300000])

def test_binary_labels():
 t=golden_tasks()[0]; labs=LabelCompiler().compile(_cube(),t,999); assert len(labs)==2; assert all(x.class_value in (0,1) for x in labs if not x.mask)

def test_ranking_is_total_and_unique():
 labs=LabelCompiler().compile(_cube(),golden_tasks()[1],999); assert sorted(x.rank for x in labs)==[1,2]

def test_treatment_choice_has_one_winner():
 labs=LabelCompiler().compile(_cube(),golden_tasks()[2],999); assert sum(x.class_value==1 for x in labs)==1; assert len({x.category_value for x in labs})==1

def test_all_task_kinds_compile_without_inference():
 from decimal import Decimal as D
 from strategy_factory_dataset_v3.contracts import LabelTaskContract
 from strategy_factory_dataset_v3.enums import UtilityDirection,LabelMaturityPolicy
 for kind in TaskKind:
  task=LabelTaskContract(f'task.{kind.value}','1.0.0',kind,'net_r',300000,'economics.baseline@1.0.0',D('0'),UtilityDirection.MAXIMIZE,(LabelMaturityPolicy.REQUIRE_RESOLVED,),quantile=D('.5') if kind==TaskKind.QUANTILE else None,bounded_min_utility=D('0') if kind==TaskKind.BOUNDED_POLICY else None)
  assert len(LabelCompiler().compile(_cube(),task,999))==2
