from saed_v4_self_supervised_pretraining.models import CorpusRecord,TrainingConfig
from saed_v4_self_supervised_pretraining.splits import assign_splits
from saed_v4_self_supervised_pretraining.tokenization import build_token_streams,build_tokenizer_spec
from saed_v4_self_supervised_pretraining.objectives import build_training_pairs,objective_registry

def setup(records,config,load):
 o=[CorpusRecord.from_mapping(x) for x in records];sp=assign_splits(o,load('lab/11_strategy_factory/examples/saed_v4_11/reference_split_policy.json'));ss=build_token_streams(o,sp);tok=build_tokenizer_spec(ss);cfg=TrainingConfig.from_mapping(config);return ss,tok,cfg

def test_registry_has_all_objectives(records,config,load):
 _,_,cfg=setup(records,config,load);r=objective_registry(cfg);assert len(r['objectives'])==7

def test_pairs_train_only(records,config,load):
 ss,t,cfg=setup(records,config,load);pairs=build_training_pairs(ss,t,cfg,cfg.curriculum[0].stage_id,0);train_ids={x.record_id for x in ss if x.split=='train'};assert pairs and {x.record_id for x in pairs}<=train_ids

def test_pairs_have_negatives(records,config,load):
 ss,t,cfg=setup(records,config,load);pairs=build_training_pairs(ss,t,cfg,cfg.curriculum[0].stage_id,0);assert all(len(x.negative_tokens)==cfg.negative_samples for x in pairs)

def test_pair_generation_deterministic(records,config,load):
 ss,t,cfg=setup(records,config,load);a=build_training_pairs(ss,t,cfg,cfg.curriculum[1].stage_id,1);b=build_training_pairs(ss,t,cfg,cfg.curriculum[1].stage_id,1);assert a==b

def test_no_outcome_objective(records,config,load):
 _,_,cfg=setup(records,config,load);assert not any('outcome' in x.objective_kind for x in cfg.objectives)
