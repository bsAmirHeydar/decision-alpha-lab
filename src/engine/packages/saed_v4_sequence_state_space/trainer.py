from __future__ import annotations
from .models import build_model
from .streaming import _dts
from .numerics import ridge_fit,ridge_predict
from .canonical import content_hash,stable_id
from .errors import TrainingError,BudgetError

def _pairs(model,sequences):
    xs=[];ys=[];ledger=[]
    for seq in sequences:
        if len(seq.points)<2:continue
        hidden,_=model.batch([p.vector for p in seq.points],_dts(seq.points))
        for i in range(len(seq.points)-1):
            xs.append(hidden[i]);ys.append(seq.points[i+1].vector);ledger.append({'sequence_id':seq.sequence_id,'input_record_id':seq.points[i].record_id,'target_record_id':seq.points[i+1].record_id,'input_known_time':seq.points[i].known_time,'target_known_time':seq.points[i+1].known_time})
    return xs,ys,ledger

def fit_candidate(spec,input_dim,sequences,max_pairs,alpha=0.01):
    model=build_model(spec,input_dim);train=[s for s in sequences if s.split=='train'];xs,ys,ledger=_pairs(model,train)
    if not xs:raise TrainingError('no training pairs')
    if len(xs)>max_pairs:raise BudgetError('training pair budget exceeded')
    weights=ridge_fit(xs,ys,alpha)
    material={'candidate_id':spec.candidate_id,'architecture':spec.architecture,'seed':spec.seed,'input_dim':input_dim,'state_dim':spec.state_dim,'context_steps':spec.context_steps,'alpha':alpha,'readout_weights':weights,'training_pair_count':len(xs),'training_pair_ledger_hash':content_hash(ledger),'core_trainable':False,'readout_trainable':True,'self_supervised_target':'next_frozen_representation'}
    checkpoint={**material,'checkpoint_id':stable_id('sequenceckpt',material),'checkpoint_hash':content_hash(material)}
    receipt={'candidate_id':spec.candidate_id,'checkpoint_hash':checkpoint['checkpoint_hash'],'pair_count':len(xs),'exposure_count':len(ledger),'ledger':ledger,'optimizer':'closed_form_ridge','deterministic':True,'receipt_id':stable_id('seqtrain',ledger),'receipt_hash':content_hash({'checkpoint_hash':checkpoint['checkpoint_hash'],'ledger':ledger})}
    return model,weights,checkpoint,receipt

def predict_next(model,weights,sequence):
    if len(sequence.points)<2:return []
    h,_=model.batch([p.vector for p in sequence.points],_dts(sequence.points));return [ridge_predict(weights,h[i]) for i in range(len(h)-1)]
