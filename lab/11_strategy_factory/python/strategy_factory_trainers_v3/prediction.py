from dataclasses import asdict
from math import isfinite
from .canonical import stable_id,canonical_sha256
from .contracts import PredictionRecord,PredictionBatch,ThresholdSelection
from .metrics import binary_metrics
from .errors import OrchestrationError
def make_batch(rows,outputs,kind,lineage,names,threshold=None):
 rows=tuple(rows);outputs=tuple(outputs)
 if len(rows)!=len(outputs):raise OrchestrationError('prediction_row_count_mismatch','prediction count differs from row count')
 rec=[]
 for row,out in zip(rows,outputs):
  out=tuple(float(x) for x in out)
  if len(out)!=len(names):raise OrchestrationError('prediction_output_width_mismatch','output width differs from task contract',{'row_id':row.row_id})
  if not all(isfinite(x) for x in out):raise OrchestrationError('non_finite_prediction','prediction contains non-finite value',{'row_id':row.row_id})
  if kind.value=='probability' and any(x<0 or x>1 for x in out):raise OrchestrationError('probability_out_of_bounds','probability outside [0,1]',{'row_id':row.row_id})
  pc=int(out[0]>=threshold) if threshold is not None else None
  mat={'row':row.row_id,'outputs':out,'lineage':asdict(lineage),'threshold':threshold}
  rec.append(PredictionRecord(stable_id('ucepred',mat),row.row_id,out,kind,lineage,threshold,pc))
 h=canonical_sha256([asdict(x) for x in rec]);return PredictionBatch(stable_id('ucebatch',h),tuple(rec),names,kind,True,h)
def select_binary_threshold(rows,batch,grid,metric,maximize):
 if not grid:grid=tuple(i/100 for i in range(5,96,5))
 y=[r.target[0] for r in rows];p=[r.outputs[0] for r in batch.records];w=[r.sample_weight for r in rows]
 scored=[(binary_metrics(y,p,w,t).get(metric,binary_metrics(y,p,w,t)['accuracy']),t) for t in grid];value,t=(max(scored) if maximize else min(scored))
 return ThresholdSelection(t,metric,value,maximize,canonical_sha256([r.row_id for r in rows]))
