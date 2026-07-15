from __future__ import annotations
from collections import defaultdict
from .canonical import content_hash, stable_id
from .models import CorpusRecord
from .errors import SplitError, LeakageError

DEFAULT_POLICY={
 "train_roots":["root_alpha","root_beta","root_gamma"],
 "validation_roots":["root_delta"],
 "test_roots":["root_epsilon"],
 "quarantine_roots":["root_canary"],
 "train_known_time_max":"2026-01-05T16:00:00Z",
 "validation_known_time_max":"2026-01-05T17:00:00Z",
 "test_known_time_max":"2026-01-05T18:00:00Z",
 "future_suffix_allowed":False,
 "descendant_cross_split_allowed":False,
}

def assign_splits(records:list[CorpusRecord], policy:dict|None=None)->dict:
    p=dict(DEFAULT_POLICY if policy is None else policy)
    root_to_split={}
    for split,key in [('train','train_roots'),('validation','validation_roots'),('test','test_roots'),('quarantine','quarantine_roots')]:
        for root in p.get(key,[]):
            if root in root_to_split: raise SplitError(f'root assigned twice: {root}')
            root_to_split[root]=split
    assignments=[]
    seen_context={}
    for r in sorted(records,key=lambda x:(x.known_time,x.record_id)):
        split=root_to_split.get(r.root_context_id)
        if split is None: raise SplitError(f'unassigned root: {r.root_context_id}')
        limit=p.get(f'{split}_known_time_max')
        if limit and r.known_time>limit: raise LeakageError(f'{split} known_time beyond cutoff: {r.record_id}')
        if r.context_id in seen_context and seen_context[r.context_id]!=split: raise LeakageError('context identity crosses split')
        seen_context[r.context_id]=split
        assignments.append({"record_id":r.record_id,"context_id":r.context_id,"root_context_id":r.root_context_id,"split":split,"event_time":r.event_time,"known_time":r.known_time})
    roots_by_split=defaultdict(set)
    for a in assignments: roots_by_split[a['split']].add(a['root_context_id'])
    split_names=sorted(roots_by_split)
    for i,a in enumerate(split_names):
        for b in split_names[i+1:]:
            if roots_by_split[a]&roots_by_split[b]: raise LeakageError('root leakage across splits')
    payload={"phase":"SAED_V4_11","policy":p,"assignments":assignments,"counts":{s:sum(1 for x in assignments if x['split']==s) for s in ['train','validation','test','quarantine']},"identity_disjoint":True,"time_bounded":True,"future_suffix_allowed":False}
    payload['split_manifest_id']=stable_id('splitmanifest',payload);payload['split_manifest_hash']=content_hash(payload)
    return payload

def split_lookup(manifest:dict)->dict[str,str]:
    return {x['record_id']:x['split'] for x in manifest['assignments']}
