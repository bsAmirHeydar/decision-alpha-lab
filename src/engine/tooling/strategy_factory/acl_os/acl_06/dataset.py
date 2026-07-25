from __future__ import annotations
import json
from datetime import datetime,timezone
from typing import Any
from .errors import ContractError,KnownTimeError
from .canonical import with_digest

def _dt(x:str)->datetime:
    d=datetime.fromisoformat(x.replace('Z','+00:00'))
    if d.tzinfo is None or d.utcoffset()!=timezone.utc.utcoffset(d): raise ContractError('UTC required')
    return d

def materialize_dataset(bundle:dict[str,Any])->dict[str,Any]:
    rows=[]
    for ds in bundle['datasets']:
        for line in ds['payload'].decode('utf-8').splitlines():
            if line.strip(): rows.append(json.loads(line))
    rows=sorted(rows,key=lambda r:(r['event_time'],r.get('symbol','')))
    cut=max(_dt(s['cut_at']) for s in bundle['dataset_set']['snapshots'])
    for r in rows:
        if _dt(r['available_at'])>cut or _dt(r['event_time'])>_dt(r['available_at']): raise KnownTimeError('dataset violates known-time order')
    return with_digest({'schema_version':'1.0.0','rows':rows,'row_count':len(rows),'known_time_verified':True},'materialized_digest')

def compile_labels(materialized:dict[str,Any],label_set:dict[str,Any])->dict[str,Any]:
    rows=materialized['rows']; out=[]
    for i,row in enumerate(rows):
        if i+1>=len(rows) or rows[i+1].get('symbol')!=row.get('symbol'):
            out.append({**row,'label_mature':False,'primary_label':None,'forward_delta':None,'diagnostic_mae':None}); continue
        nxt=rows[i+1]; delta=float(nxt['feature_x'])-float(row['feature_x'])
        out.append({**row,'label_mature':True,'primary_label':'UP' if delta>0 else 'NOT_UP','forward_delta':delta,'diagnostic_mae':min(0.0,delta)})
    return with_digest({'schema_version':'1.0.0','rows':out,'row_count':len(out),'mature_count':sum(1 for r in out if r['label_mature']),'diagnostic_labels_segregated':True},'label_frame_digest')

def assign_splits(label_frame:dict[str,Any],split:dict[str,Any])->dict[str,Any]:
    out=[]
    for row in label_frame['rows']:
        t=_dt(row['event_time']); segment='UNASSIGNED'
        for name in ('train','validation','test'):
            if _dt(split[name]['start'])<=t<=_dt(split[name]['end']): segment=name.upper(); break
        out.append({**row,'segment':segment})
    counts={s:sum(1 for r in out if r['segment']==s) for s in ('TRAIN','VALIDATION','TEST','UNASSIGNED')}
    return with_digest({'schema_version':'1.0.0','rows':out,'row_count':len(out),'segment_counts':counts,'purge_seconds':split['purge_seconds'],'embargo_seconds':split['embargo_seconds'],'transform_fit_scope':split['transform_fit_scope'],'known_time_verified':True},'split_frame_digest')
