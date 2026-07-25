import pytest
from strategy_factory_trainers_v3 import *
from strategy_factory_trainers_v3.golden import build_case
class Failing(PriorBinaryTrainer):
 @classmethod
 def capability(cls):
  d=PriorBinaryTrainer.capability();return TrainerCapabilityDescriptor('uce.test.failing','1.0.0','test_failure',d.supported_tasks,d.supported_views,d.supported_target_shapes)
 def fit(self,d):raise RuntimeError('injected fit failure')
def test_failed_trial_is_retained_on_exception():
 r=TrainerRegistry();r.register(Failing);s,rows,p=build_case(TaskKind.BINARY_CLASSIFICATION);p=OrchestrationPlan(p.plan_id,p.plan_version,p.task,TrainerConfig('uce.test.failing','1.0.0',{},7),p.resources,p.oof)
 with pytest.raises(OrchestrationRunFailed) as e:TaskOrchestrator(r).run(p,s,rows)
 assert len(e.value.trial_ledger)==1 and e.value.trial_ledger[0].status is TrialStatus.FAILED
def test_cancelled_admission_is_retained():
 r=TrainerRegistry();register_reference_trainers(r);s,rows,p=build_case(TaskKind.REGRESSION);token=CancellationToken();token.cancel('operator')
 with pytest.raises(OrchestrationRunFailed) as e:TaskOrchestrator(r).run(p,s,rows,cancel_token=token)
 assert e.value.trial_ledger[0].status is TrialStatus.CANCELLED
