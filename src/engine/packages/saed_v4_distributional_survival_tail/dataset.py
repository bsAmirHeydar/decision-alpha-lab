from __future__ import annotations
from datetime import datetime,timedelta,timezone
import math
from .canonical import content_hash,stable_id,hash_signed,hash_unit,seal
from .numerics import clamp

def _iso(dt):return dt.astimezone(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
def _split(i,spec):
    if i<spec.train_rows:return 'train'
    if i<spec.train_rows+spec.calibration_rows:return 'calibration'
    return 'selection_validation'

def build(upstream,fusion_outputs,spec,event_registry,censoring):
    champ=upstream['reference_fusion_candidate_id'];base=next(x['fused_embedding'] for x in fusion_outputs['items'] if x['candidate_id']==champ)
    start=datetime.fromisoformat(spec.start_time.replace('Z','+00:00'));causes=event_registry.causes;rows=[]
    for i in range(spec.row_count):
        known=start+timedelta(seconds=i*spec.spacing_seconds);signal=sum(base[k]*(k+1) for k in range(len(base)))/len(base)+0.35*math.sin(i/11)+0.18*hash_signed(f'{spec.seed}:signal:{i}')
        features=[float(format(base[k]+0.13*math.sin((i+1)*(k+1)/17)+0.07*hash_signed(f'{spec.seed}:f:{i}:{k}'),'.15g')) for k in range(spec.feature_dim)]
        u=hash_unit(f'{spec.seed}:cause:{i}');cause=causes[min(len(causes)-1,int(u*len(causes)))]
        # Explicit heavy-tail and zero/non-fill mass generation; deterministic synthetic evidence only.
        raw=hash_signed(f'{spec.seed}:r:{i}');tail=math.tan(math.pi*(clamp(hash_unit(f'{spec.seed}:tail:{i}'),.01,.99)-.5))
        net=0.55*signal+0.32*raw+0.16*tail
        if cause in {'cancellation','expiry','invalidation'}:net*=.15
        if cause=='stop':net=-abs(net)-.65
        if cause=='target':net=abs(net)+.75
        if cause=='trail_exit':net=abs(net)+.25
        net=clamp(net,-8,12)
        latent=45+int(3555*hash_unit(f'{spec.seed}:time:{i}'))
        observed=latent<censoring.administrative_horizon_seconds and (i%9!=0)
        duration=min(latent,censoring.administrative_horizon_seconds)
        final_cause=cause if observed else event_registry.censor_label
        interval=censoring.observation_interval_seconds
        lower=(duration//interval)*interval;upper=min(censoring.administrative_horizon_seconds,lower+interval)
        if not censoring.allow_interval_censoring or i%4:lower=duration;upper=duration
        outcome_observed=observed and final_cause not in {'cancellation','expiry','invalidation'}
        if not outcome_observed:net=0.0
        mfe=max(0.0,net+abs(hash_signed(f'{spec.seed}:mfe:{i}'))*1.1);mae=-max(0.0,-net+abs(hash_signed(f'{spec.seed}:mae:{i}'))*.9)
        giveback=max(0.0,mfe-max(0.0,net));row={'row_id':stable_id('v416row',{'i':i,'seed':spec.seed}),'ordinal':i,'split':_split(i,spec),'context_time':_iso(known),'feature_known_time':_iso(known),'outcome_known_time':_iso(known+timedelta(seconds=duration)),'known_as_of':_iso(known),'source_fusion_hash':upstream['v4_15_fusion_hash'],'source_registry_hash':upstream['v4_15_registry_hash'],'feature_dim':spec.feature_dim,'features':features,'event_duration_seconds':duration,'interval_lower_seconds':lower,'interval_upper_seconds':upper,'event_observed':observed,'event_cause':final_cause,'outcome_observed':outcome_observed,'net_r':float(format(net,'.15g')),'mfe_r':float(format(mfe,'.15g')),'mae_r':float(format(mae,'.15g')),'hold_seconds':duration,'giveback_r':float(format(giveback,'.15g')),'capital_time':float(format(duration*(1+abs(net)),'.15g')),'synthetic':True,'future_suffix_accessed':False,'production_eligible':False}
        row['row_hash']=content_hash(row);rows.append(row)
    artifact={'phase':'SAED_V4_16','dataset_id':stable_id('v416dataset',{'rows':[r['row_hash'] for r in rows],'spec':spec.__dict__}),'row_count':len(rows),'feature_dim':spec.feature_dim,'split_counts':{s:sum(r['split']==s for r in rows) for s in ['train','calibration','selection_validation']},'event_counts':{c:sum(r['event_cause']==c for r in rows) for c in list(event_registry.causes)+[event_registry.censor_label]},'known_time_ordered':all(rows[i]['context_time']<rows[i+1]['context_time'] for i in range(len(rows)-1)),'chronological_split':True,'synthetic_only':True,'protected_evidence_exposures':0,'rows':rows}
    artifact['dataset_hash']=content_hash(artifact);return artifact
