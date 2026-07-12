import pytest
from strategy_factory_trainers_v3 import *
from strategy_factory_trainers_v3.golden import build_case
def test_test_seal_and_access_audit():
 s,rows,p=build_case(TaskKind.BINARY_CLASSIFICATION);d=GuardedDataset(s,rows)
 with pytest.raises(DataAccessError):d.view(p.oof.final_test_row_ids,SplitRole.FINAL_TEST,AccessPurpose.PREDICT_FINAL_TEST,OrchestrationPhase.FINAL_TEST,p.trainer.key,'final')
 d.lock_selection();assert len(d.view(p.oof.final_test_row_ids,SplitRole.FINAL_TEST,AccessPurpose.PREDICT_FINAL_TEST,OrchestrationPhase.FINAL_TEST,p.trainer.key,'final').rows)==4;assert not d.audit[0].allowed and d.audit[1].allowed
def test_lifecycle_restart_parity():
 s,rows,p=build_case(TaskKind.BINARY_CLASSIFICATION);d=GuardedDataset(s,rows);x=TrainerSession(PriorBinaryTrainer());x.configure(p.trainer,p.resources);x.validate(p.task,s);m=x.fit(d.view(p.oof.folds[0].train_row_ids,SplitRole.TRAIN,AccessPurpose.FIT,OrchestrationPhase.FOLD_TRAINING,p.trainer.key,'fold0'));assert PriorBinaryTrainer().load(x.serialize()).state_hash==m.state_hash;x.dispose();assert x.state is TrainerLifecycleState.DISPOSED

def test_final_test_is_one_shot_after_lock():
 s,rows,p=build_case(TaskKind.BINARY_CLASSIFICATION);d=GuardedDataset(s,rows);d.lock_selection();d.view(p.oof.final_test_row_ids,SplitRole.FINAL_TEST,AccessPurpose.PREDICT_FINAL_TEST,OrchestrationPhase.FINAL_TEST,p.trainer.key,'final')
 with pytest.raises(DataAccessError):d.view(p.oof.final_test_row_ids,SplitRole.FINAL_TEST,AccessPurpose.PREDICT_FINAL_TEST,OrchestrationPhase.FINAL_TEST,p.trainer.key,'final')
