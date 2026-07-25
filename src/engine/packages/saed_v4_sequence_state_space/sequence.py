from __future__ import annotations
from datetime import datetime
from .contracts import SequencePoint,SequenceExample
from .canonical import content_hash,stable_id
from .errors import CausalityError,ContractError

def _dt(s): return datetime.fromisoformat(str(s).replace('Z','+00:00'))

def compile_points(token_stream_document:dict,embedding_table)->tuple[SequencePoint,...]:
    points=[]
    for raw in token_stream_document['streams']:
        if raw['known_time']<raw['event_time']: raise CausalityError('known_time precedes event_time')
        tokens=tuple(map(str,raw['tokens']))
        forbidden=[t for t in tokens if t.startswith('OUTCOME::') or t.startswith('EXECUTION_RESULT::') or t.startswith('CONTEXT_ID::') or t.startswith('RECORD_ID::')]
        if forbidden: raise CausalityError(f'forbidden sequence token: {forbidden[0]}')
        points.append(SequencePoint(str(raw['record_id']),str(raw['context_id']),str(raw['root_context_id']),str(raw['domain_id']),str(raw['event_time']),str(raw['known_time']),str(raw['split']),embedding_table.stream(tokens),str(raw['token_hash'])))
    return tuple(points)

def compile_sequences(points,max_context_steps:int)->tuple[SequenceExample,...]:
    groups={}
    for p in points:
        if p.split=='quarantine':continue
        groups.setdefault((p.root_context_id,p.split),[]).append(p)
    out=[]
    for (root,split),rows in sorted(groups.items()):
        domains=sorted({x.domain_id for x in rows})
        domain=domains[0] if len(domains)==1 else 'MULTI_DOMAIN'
        rows.sort(key=lambda x:(x.event_time,x.known_time,x.record_id))
        if any(rows[i].event_time>=rows[i+1].event_time for i in range(len(rows)-1)): raise CausalityError('non-monotone sequence event time')
        rows=rows[-max_context_steps:]
        material={'root_context_id':root,'domain_id':domain,'split':split,'record_ids':[x.record_id for x in rows],'token_hashes':[x.token_hash for x in rows]}
        out.append(SequenceExample(stable_id('seq',material),root,domain,split,tuple(rows),content_hash(material)))
    return tuple(out)

def sequence_manifest(sequences,upstream_hashes:dict)->dict:
    material={'phase':'SAED_V4_12','sequence_ids':[s.sequence_id for s in sequences],'source_hashes':[s.source_hash for s in sequences],'upstream_hashes':upstream_hashes,'future_suffix_allowed':False,'identity_tokens_allowed':False,'outcome_inputs_allowed':False}
    return {**material,'sequence_count':len(sequences),'split_counts':{k:sum(s.split==k for s in sequences) for k in ('train','validation','test')},'manifest_id':stable_id('v412sequences',material),'manifest_hash':content_hash(material)}

def sequence_to_dict(s):
    return {'sequence_id':s.sequence_id,'root_context_id':s.root_context_id,'domain_id':s.domain_id,'split':s.split,'source_hash':s.source_hash,'points':[{'record_id':p.record_id,'context_id':p.context_id,'root_context_id':p.root_context_id,'domain_id':p.domain_id,'event_time':p.event_time,'known_time':p.known_time,'split':p.split,'vector':list(p.vector),'token_hash':p.token_hash} for p in s.points]}
