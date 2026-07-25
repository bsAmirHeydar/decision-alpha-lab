from dataclasses import asdict
from time import monotonic
from .canonical import stable_id,canonical_sha256
from .contracts import *
from .data_access import GuardedDataset
from .enums import *
from .resources import BudgetGuard,CancellationToken
from .lifecycle import TrainerSession
from .prediction import select_binary_threshold
from .metrics import binary_metrics,regression_metrics,ranking_metrics
from .artifacts import ArtifactPackager
from .telemetry import TelemetrySink
from .errors import OrchestrationError,ResourceBudgetError,OrchestrationRunFailed
class TaskOrchestrator:
 def __init__(self,registry):self.registry=registry.freeze()
 def lineage(self,s,t,c,fold,m,role,phase):return PredictionLineage(s.dataset_id,s.dataset_manifest_hash,t.key,c.key,c.config_hash,fold,c.seed,m.state_hash,role,phase)
 def metrics(self,t,rows,batch,threshold=.5):
  y=[r.target[0] for r in rows];p=[x.outputs[0] for x in batch.records];w=[r.sample_weight for r in rows]
  if t.task_kind is TaskKind.BINARY_CLASSIFICATION:return binary_metrics(y,p,w,threshold)
  if t.task_kind is TaskKind.REGRESSION:return regression_metrics(y,p,w)
  if t.task_kind is TaskKind.RANKING:return ranking_metrics(y,p,[r.ranking_group for r in rows],w)
  return {t.primary_metric:0.}
 def _terminal_status(self,e):
  code=getattr(getattr(e,'context',None),'code',type(e).__name__)
  if code=='training_timed_out':return TrialStatus.TIMED_OUT,code
  if code=='training_cancelled':return TrialStatus.CANCELLED,code
  return TrialStatus.FAILED,code
 def _raise(self,code,message,trials,ds,tele,details=None):raise OrchestrationRunFailed(code,message,tuple(trials),ds.audit if ds else (),tele.events if tele else (),details)
 def run(self,plan,schema,rows,code_hash='unknown',cancel_token=None):
  if schema.row_count!=len(rows):raise OrchestrationError('row_count_mismatch','schema and rows differ')
  ds=GuardedDataset(schema,rows);tele=TelemetrySink();trials=[];seq=0;entry=self.registry.resolve_exact(plan.trainer.trainer_id,plan.trainer.trainer_version);guard=BudgetGuard(plan.resources,schema,cancel_token or CancellationToken())
  try:guard.start()
  except Exception as e:
   status,err=self._terminal_status(e);trials.append(TrialLedgerEntry(stable_id('ucetrial',{'plan':plan.plan_hash,'fold':'admission'}),plan.plan_hash,entry.descriptor.key,'admission',status,0,1,0,{},'','',err,str(e),''));self._raise('training_admission_failed','resource admission failed',trials,ds,tele,{'error':err})
  tele.emit(OrchestrationPhase.PREFLIGHT,entry.descriptor.key,'global','preflight_passed','info',schema.row_count,len(schema.feature_order))
  oof=[]
  for fold in plan.oof.folds:
   seq+=1;started=monotonic();session=TrainerSession(entry.factory());model=batch=None;status=TrialStatus.RUNNING;metrics={};err='';failure_message=''
   tid=stable_id('ucetrial',{'plan':plan.plan_hash,'fold':fold.fold_id,'trainer':entry.descriptor.key})
   try:
    session.configure(plan.trainer,plan.resources);session.validate(plan.task,schema);train=ds.view(fold.train_row_ids,SplitRole.TRAIN,AccessPurpose.FIT,OrchestrationPhase.FOLD_TRAINING,entry.descriptor.key,fold.fold_id);guard.poll();model=session.fit(train);guard.poll()
    if fold.calibration_row_ids and plan.trainer.calibration_kind is not CalibrationKind.NONE:session.calibrate(ds.view(fold.calibration_row_ids,SplitRole.CALIBRATION,AccessPurpose.CALIBRATE,OrchestrationPhase.FOLD_CALIBRATION,entry.descriptor.key,fold.fold_id),plan.trainer.calibration_kind)
    hold=ds.view(fold.holdout_row_ids,SplitRole.OOF_HOLDOUT,AccessPurpose.PREDICT_OOF,OrchestrationPhase.OOF_PREDICTION,entry.descriptor.key,fold.fold_id);batch=session.predict(hold,self.lineage(schema,plan.task,plan.trainer,fold.fold_id,model,SplitRole.OOF_HOLDOUT,OrchestrationPhase.OOF_PREDICTION));oof.extend(batch.records);metrics=self.metrics(plan.task,hold.rows,batch);loaded=entry.factory().load(session.serialize())
    if loaded.state_hash!=model.state_hash:raise OrchestrationError('serialization_parity_failed','state mismatch')
    status=TrialStatus.SUCCEEDED
   except Exception as e:session.fail();status,err=self._terminal_status(e);failure_message=str(e)
   elapsed=int((monotonic()-started)*1000);seq+=1;trials.append(TrialLedgerEntry(tid,plan.plan_hash,entry.descriptor.key,fold.fold_id,status,seq-1,seq,elapsed,metrics,model.state_hash if model else '',batch.evidence_hash if batch else '',err,failure_message if status is not TrialStatus.SUCCEEDED else '',''));session.dispose()
   if status is not TrialStatus.SUCCEEDED:self._raise('fold_training_failed','fold failed',trials,ds,tele,{'error':err,'fold_id':fold.fold_id})
  oofh=canonical_sha256([asdict(x) for x in oof]);oofb=PredictionBatch(stable_id('uceoof',oofh),tuple(oof),plan.task.output_names,plan.task.prediction_kind,True,oofh);ds.lock_selection();tele.emit(OrchestrationPhase.SELECTION_LOCK,entry.descriptor.key,'global','selection_locked','info',0,len(schema.feature_order))
  started=monotonic();session=TrainerSession(entry.factory());threshold=None;model=None;testb=None;manifest=card=None;finalmetrics={};status=TrialStatus.RUNNING;err='';failure_message=''
  try:
   session.configure(plan.trainer,plan.resources);session.validate(plan.task,schema);train=ds.view(plan.oof.final_train_row_ids,SplitRole.FINAL_TRAIN,AccessPurpose.FIT,OrchestrationPhase.FINAL_TRAINING,entry.descriptor.key,'final');guard.poll();model=session.fit(train)
   if plan.oof.final_calibration_row_ids and plan.trainer.calibration_kind is not CalibrationKind.NONE:session.calibrate(ds.view(plan.oof.final_calibration_row_ids,SplitRole.FINAL_CALIBRATION,AccessPurpose.CALIBRATE,OrchestrationPhase.FINAL_CALIBRATION,entry.descriptor.key,'final'),plan.trainer.calibration_kind)
   if plan.task.threshold_selection_required and plan.oof.final_threshold_row_ids:
    th=ds.view(plan.oof.final_threshold_row_ids,SplitRole.FINAL_THRESHOLD,AccessPurpose.SELECT_THRESHOLD,OrchestrationPhase.FINAL_THRESHOLD,entry.descriptor.key,'final');thb=session.predict(th,self.lineage(schema,plan.task,plan.trainer,'final_threshold',model,SplitRole.FINAL_THRESHOLD,OrchestrationPhase.FINAL_THRESHOLD));threshold=select_binary_threshold(th.rows,thb,plan.trainer.threshold_grid,plan.trainer.threshold_metric or 'accuracy',True)
   test=ds.view(plan.oof.final_test_row_ids,SplitRole.FINAL_TEST,AccessPurpose.PREDICT_FINAL_TEST,OrchestrationPhase.FINAL_TEST,entry.descriptor.key,'final');testb=session.predict(test,self.lineage(schema,plan.task,plan.trainer,'final',model,SplitRole.FINAL_TEST,OrchestrationPhase.FINAL_TEST))
   if threshold:
    rec=tuple(PredictionRecord(x.prediction_id,x.row_id,x.outputs,x.prediction_kind,x.lineage,threshold.threshold,int(x.outputs[0]>=threshold.threshold)) for x in testb.records);testb=PredictionBatch(testb.batch_id,rec,testb.output_names,testb.prediction_kind,True,canonical_sha256([asdict(x) for x in rec]))
   finalmetrics=self.metrics(plan.task,test.rows,testb,threshold.threshold if threshold else .5);manifest,card=ArtifactPackager.package(entry.descriptor,plan.trainer,plan.task,schema,plan.oof,plan.resources,model,session.serialize(),session.calibration,threshold,finalmetrics,code_hash,('Reference trainer; replace with I08+ production plugin.',));status=TrialStatus.SUCCEEDED
  except Exception as e:session.fail();status,err=self._terminal_status(e);failure_message=str(e)
  finally:session.dispose()
  final=TrialLedgerEntry(stable_id('ucetrial',{'plan':plan.plan_hash,'fold':'final'}),plan.plan_hash,entry.descriptor.key,'final',status,seq+1,seq+2,int((monotonic()-started)*1000),finalmetrics,model.state_hash if model else '',testb.evidence_hash if testb else '',err,failure_message if status is not TrialStatus.SUCCEEDED else '','')
  if status is not TrialStatus.SUCCEEDED:self._raise('final_training_failed','final path failed',trials+[final],ds,tele,{'error':err})
  rid=stable_id('ucerun',{'plan':plan.plan_hash,'oof':oofb.evidence_hash,'test':testb.evidence_hash});return OrchestrationResult(rid,plan.plan_hash,oofb,testb,threshold,tuple(trials),final,manifest,card,ds.audit,tele.events,True)
