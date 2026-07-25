from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from .models import TokenStream, TrainingConfig
from .masking import deterministic_mask_positions
from .negatives import sample_token_negatives, sample_temporal_negative
from .canonical import content_hash, stable_id, hash_unit

@dataclass(frozen=True)
class TrainingPair:
    objective_id: str
    objective_kind: str
    anchor_token: str
    positive_token: str
    negative_tokens: tuple[str,...]
    record_id: str
    weight: float

def _limited(items:list[TrainingPair], limit:int, key:str)->list[TrainingPair]:
    return sorted(items,key=lambda x:(hash_unit(key+'|'+x.anchor_token+'|'+x.positive_token+'|'+x.record_id),x.anchor_token,x.positive_token))[:limit]

def build_training_pairs(streams:list[TokenStream], tokenizer:dict, config:TrainingConfig, stage_id:str, epoch:int)->list[TrainingPair]:
    stage=next(x for x in config.curriculum if x.stage_id==stage_id)
    objective_by_id={x.objective_id:x for x in config.objectives if x.enabled}
    train=[s for s in streams if s.split=='train']
    ordered=sorted(train,key=lambda s:(s.known_time,s.record_id))
    pairs=[]
    for s in ordered:
        local=[]
        non_special=[t for t in s.tokens if not t.startswith('[')]
        by_view=defaultdict(list)
        for t in non_special:
            if t.startswith('VIEW::'):
                parts=t.split('::',3);by_view[parts[1]].append(t)
        for oid in stage.objective_ids:
            spec=objective_by_id[oid]
            kind=spec.objective_kind
            if kind=='masked_span':
                positions=deterministic_mask_positions(s,config.seed+epoch,0.18)
                visible=[t for i,t in enumerate(s.tokens) if i not in positions and not t.startswith('[')]
                for pos in positions:
                    target=s.tokens[pos]
                    if visible:
                        anchor=visible[int(hash_unit(f'{s.record_id}|{epoch}|{pos}')*len(visible))%len(visible)]
                        neg=sample_token_negatives(tokenizer['vocabulary'],target,config.negative_samples,f'{oid}|{s.record_id}|{epoch}|{pos}')
                        local.append(TrainingPair(oid,kind,anchor,target,tuple(neg),s.record_id,spec.weight))
            elif kind=='cross_view_alignment':
                views=sorted(k for k,v in by_view.items() if v)
                for i in range(len(views)-1):
                    a=by_view[views[i]][0];p=by_view[views[i+1]][0]
                    neg=sample_token_negatives(tokenizer['vocabulary'],p,config.negative_samples,f'{oid}|{s.record_id}|{epoch}|{i}')
                    local.append(TrainingPair(oid,kind,a,p,tuple(neg),s.record_id,spec.weight))
            elif kind=='graph_relation_reconstruction':
                rel=[t for t in non_special if t.startswith('GRAPH_REL::')]
                views=[t for t in non_special if t.startswith('VIEW::')]
                for i,r in enumerate(rel[:4]):
                    if views:
                        a=views[i%len(views)];neg=sample_token_negatives(tokenizer['vocabulary'],r,config.negative_samples,f'{oid}|{s.record_id}|{epoch}|{i}')
                        local.append(TrainingPair(oid,kind,a,r,tuple(neg),s.record_id,spec.weight))
            elif kind=='missingness_reconstruction':
                masks=[t for t in non_special if t.startswith('VIEW_MASK::')]
                kinds=[t for t in non_special if t.startswith('VIEW_KIND::')]
                for i,m in enumerate(masks):
                    if kinds:
                        a=kinds[i%len(kinds)];neg=sample_token_negatives(tokenizer['vocabulary'],m,config.negative_samples,f'{oid}|{s.record_id}|{epoch}|{i}')
                        local.append(TrainingPair(oid,kind,a,m,tuple(neg),s.record_id,spec.weight))
            elif kind in {'next_event','context_transition','temporal_contrast'}:
                idx=ordered.index(s)
                future=[x for x in ordered[idx+1:] if x.root_context_id==s.root_context_id]
                if future:
                    nxt=future[0]
                    a=next((t for t in non_special if t.startswith('VIEW::')),non_special[0])
                    pos=next((t for t in nxt.tokens if t.startswith('VIEW::')),next(t for t in nxt.tokens if not t.startswith('[')))
                    neg_record=sample_temporal_negative(s,streams,f'{oid}|{s.record_id}|{epoch}')
                    neg_token=next((t for t in neg_record.tokens if t.startswith('VIEW::')),next(t for t in neg_record.tokens if not t.startswith('[')))
                    extra=sample_token_negatives(tokenizer['vocabulary'],pos,max(0,config.negative_samples-1),f'{oid}|{s.record_id}|extra') if config.negative_samples>1 else []
                    local.append(TrainingPair(oid,kind,a,pos,tuple([neg_token]+extra),s.record_id,spec.weight))
        pairs.extend(_limited(local,stage.max_pairs_per_record,f'{config.seed}|{stage_id}|{epoch}|{s.record_id}'))
    return pairs

def objective_registry(config:TrainingConfig)->dict:
    payload={"phase":"SAED_V4_11","objectives":[{"objective_id":x.objective_id,"objective_kind":x.objective_kind,"weight":x.weight,"enabled":x.enabled,"outcome_supervised":False} for x in config.objectives],"curriculum":[{"stage_id":x.stage_id,"epochs":x.epochs,"objective_ids":list(x.objective_ids),"max_pairs_per_record":x.max_pairs_per_record} for x in config.curriculum],"forbidden_objectives":["outcome_prediction","treatment_ranking","policy_value","live_fill_prediction"]}
    payload['registry_id']=stable_id('objectiveregistry',payload);payload['registry_hash']=content_hash(payload);return payload
