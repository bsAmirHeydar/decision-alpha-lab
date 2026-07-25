from __future__ import annotations
from .canonical import content_hash,stable_id
from .errors import LeakageError

def build_chronological_cluster_folds(dataset,plan):
    n=dataset['row_count'];folds=[];width=max(40,(n//(plan.cross_fit_folds+2))//2*2);start=n-plan.cross_fit_folds*width
    for k in range(plan.cross_fit_folds):
        eval_start=start+k*width;eval_end=min(n,eval_start+width);train_end=max(0,eval_start-plan.purge_rows-plan.embargo_rows)
        train=list(range(0,train_end));evaluation=list(range(eval_start,eval_end))
        folds.append({'fold_id':f'fold_{k}','train_ordinals':train,'evaluation_ordinals':evaluation,'train_end':train_end-1 if train else -1,'evaluation_start':eval_start,'evaluation_end':eval_end-1,'purge_rows':plan.purge_rows,'embargo_rows':plan.embargo_rows})
    out={'phase':'SAED_V4_18','split_plan_id':stable_id('v418_split',{'dataset':dataset['dataset_hash'],'folds':folds}),'chronological':True,'cluster_aware':True,'future_training_forbidden':True,'sibling_split_forbidden':True,'fold_count':len(folds),'folds':folds}
    out['split_hash']=content_hash(out);return out

def audit_splits(dataset,split_plan):
    by_cluster={}
    for r in dataset['rows']:by_cluster.setdefault(r['cluster_id'],set()).add(r['ordinal'])
    audits=[]
    for f in split_plan['folds']:
        tr=set(f['train_ordinals']);ev=set(f['evaluation_ordinals']);future=bool(tr and ev and max(tr)>=min(ev));siblings=sum(1 for ords in by_cluster.values() if ords&tr and ords&ev)
        audits.append({'fold_id':f['fold_id'],'train_rows':len(tr),'evaluation_rows':len(ev),'overlap_rows':len(tr&ev),'future_training_detected':future,'sibling_cluster_splits':siblings,'passed':not(tr&ev) and not future and siblings==0})
    out={'phase':'SAED_V4_18','fold_count':len(audits),'audits':audits,'passed':all(x['passed'] for x in audits)};out['audit_hash']=content_hash(out);return out
