from strategy_factory_deep_views_v3.registry import DeepAlgorithmRegistry
from strategy_factory_deep_views_v3.trainer_plugins import register_deep_trainers,CausalTemporalConvTrainer
from strategy_factory_trainers_v3.registry import TrainerRegistry
from strategy_factory_trainers_v3.contracts import TrainerConfig,ResourceBudget,DatasetSchema,TaskContract,TrainingRow,PredictionLineage
from strategy_factory_trainers_v3.data_access import DataView
from strategy_factory_trainers_v3.enums import *
from strategy_factory_deep_views_v3.golden import sequence_case
def test_registry_is_exact_and_frozen():
    snap=DeepAlgorithmRegistry().freeze().snapshot();assert snap.frozen;assert len(snap.descriptors)==17;assert len({x.key for x in snap.descriptors})==17
def test_deep_trainers_register_and_sequence_serializes():
    registry=TrainerRegistry();keys=register_deep_trainers(registry);assert len(keys)==5
    values,targets,shape=sequence_case(12);rows=tuple(TrainingRow(f'r{i}',v,t,SplitRole.TRAIN,'f','c',i,i) for i,(v,t) in enumerate(zip(values,targets)))
    plugin=CausalTemporalConvTrainer();config=TrainerConfig('uce.deep.causal_temporal_conv_ridge','1.0.0',{'steps':shape[0],'channels':shape[1],'known_time_audit_passed':True,'deep_admission_decision':'accept'},7);resources=ResourceBudget(7);task=TaskContract('t','1',TaskKind.REGRESSION,ViewKind.SEQUENCE,TargetShape.SCALAR,PredictionKind.VALUE,'rmse',False);schema=DatasetSchema('d','m',tuple(f'f{i}' for i in range(shape[0]*shape[1])),ViewKind.SEQUENCE,TensorKind.DENSE_FLOAT64,TargetShape.SCALAR,1,False,True,False,len(rows))
    plugin.configure(config,resources);plugin.validate(task,schema);view=DataView('d','m',schema.feature_order,rows,SplitRole.TRAIN,'f',AccessPurpose.FIT);model=plugin.fit(view);loaded=plugin.load(plugin.serialize(model));assert loaded.state_hash==model.state_hash
