from .registry import TrainerRegistry
from .reference_trainers import register_reference_trainers,PriorBinaryTrainer
from .orchestrator import TaskOrchestrator
from .golden import build_case
from .contracts import *
from .enums import *
from .data_access import GuardedDataset
from .resources import CancellationToken
from .errors import DataAccessError,OrchestrationRunFailed
from .canonical import canonical_sha256
class _FailingReference(PriorBinaryTrainer):
 @classmethod
 def capability(cls):
  d=PriorBinaryTrainer.capability();return TrainerCapabilityDescriptor('uce.conformance.failing','1.0.0','conformance_failure',d.supported_tasks,d.supported_views,d.supported_target_shapes)
 def fit(self,data):raise RuntimeError('conformance injected failure')
def run_conformance():
 r=TrainerRegistry();register_reference_trainers(r);o=TaskOrchestrator(r);cases=[]
 for task in (TaskKind.BINARY_CLASSIFICATION,TaskKind.REGRESSION,TaskKind.RANKING):
  s,rows,p=build_case(task);a=o.run(p,s,rows,'conformance');b=o.run(p,s,rows,'conformance');cases.append({'task':task.value,'trainer':p.trainer.key,'deterministic':a.oof_predictions.evidence_hash==b.oof_predictions.evidence_hash and a.final_test_predictions.evidence_hash==b.final_test_predictions.evidence_hash,'lineage_complete':all(x.lineage.dataset_manifest_hash==s.dataset_manifest_hash for x in a.oof_predictions.records+a.final_test_predictions.records),'ledger_retained':all(x.status is TrialStatus.SUCCEEDED for x in a.fold_trials+(a.final_trial,)),'oof_count':len(a.oof_predictions.records),'test_count':len(a.final_test_predictions.records),'artifact_id':a.artifact_manifest.artifact_id})
 s,rows,p=build_case(TaskKind.BINARY_CLASSIFICATION);d=GuardedDataset(s,rows);sealed=False
 try:d.view(p.oof.final_test_row_ids,SplitRole.FINAL_TEST,AccessPurpose.PREDICT_FINAL_TEST,OrchestrationPhase.FINAL_TEST,p.trainer.key,'final')
 except DataAccessError:sealed=True
 d.lock_selection();d.view(p.oof.final_test_row_ids,SplitRole.FINAL_TEST,AccessPurpose.PREDICT_FINAL_TEST,OrchestrationPhase.FINAL_TEST,p.trainer.key,'final');one_shot=False
 try:d.view(p.oof.final_test_row_ids,SplitRole.FINAL_TEST,AccessPurpose.PREDICT_FINAL_TEST,OrchestrationPhase.FINAL_TEST,p.trainer.key,'final')
 except DataAccessError:one_shot=True
 bad=False
 try:o.run(OrchestrationPlan('bad','1.0.0',p.task,TrainerConfig('uce.reference.mean_regression','1.0.0',{},7),p.resources,p.oof),s,rows)
 except Exception:bad=True
 fr=TrainerRegistry();fr.register(_FailingReference);fp=OrchestrationPlan('failure','1.0.0',p.task,TrainerConfig('uce.conformance.failing','1.0.0',{},7),p.resources,p.oof);failed_retained=False
 try:TaskOrchestrator(fr).run(fp,s,rows)
 except OrchestrationRunFailed as e:failed_retained=len(e.trial_ledger)==1 and e.trial_ledger[0].status is TrialStatus.FAILED
 s2,rows2,p2=build_case(TaskKind.REGRESSION);token=CancellationToken();token.cancel('conformance');cancelled_retained=False
 try:o.run(p2,s2,rows2,cancel_token=token)
 except OrchestrationRunFailed as e:cancelled_retained=bool(e.trial_ledger) and e.trial_ledger[0].status is TrialStatus.CANCELLED
 out={'release':'UCE-I07','registry_size':len(r.snapshot()),'cases':cases,'test_seal_enforced':sealed,'final_test_one_shot':one_shot,'unsupported_pair_rejected':bad,'failed_trial_retained':failed_retained,'cancelled_trial_retained':cancelled_retained};out['evidence_hash']=canonical_sha256(out);out['passed']=all(x['deterministic'] and x['lineage_complete'] and x['ledger_retained'] for x in cases) and sealed and one_shot and bad and failed_retained and cancelled_retained;return out
