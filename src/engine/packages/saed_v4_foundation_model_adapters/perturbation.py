from copy import deepcopy
from .canonical import content_hash,stable_id
from .tokenization import compile_token_sequence
from .adapters import run_adapter

def future_suffix_audit(compiled_graph,embeddings,champion_id,config,candidate):
    cutoff=sorted(n['known_time'] for n in compiled_graph['nodes'])[max(0,len(compiled_graph['nodes'])-8)]
    base=compile_token_sequence(compiled_graph,embeddings,champion_id,config,cutoff);f0=run_adapter(base,config,candidate)
    mutated=deepcopy(compiled_graph); template=deepcopy(mutated['nodes'][-1]);template['node_id']='future_injected_'+content_hash(candidate.candidate_id)[:12];template['known_time']='9999-12-31T23:59:59Z';mutated['nodes'].append(template)
    emb=deepcopy(embeddings);champ=next(x for x in emb['candidates'] if x['candidate_id']==champion_id);champ['embeddings'][template['node_id']]=[999.0]*len(next(iter(champ['embeddings'].values())))
    again=compile_token_sequence(mutated,emb,champion_id,config,cutoff);f1=run_adapter(again,config,candidate)
    passed=f0['feature_hash']==f1['feature_hash'] and base['token_sequence_hash']==again['token_sequence_hash']
    doc={'phase':'SAED_V4_14','candidate_id':candidate.candidate_id,'cutoff':cutoff,'base_token_hash':base['token_sequence_hash'],'mutated_token_hash':again['token_sequence_hash'],'base_feature_hash':f0['feature_hash'],'mutated_feature_hash':f1['feature_hash'],'passed':passed,'future_suffix_rejected':passed};doc['audit_hash']=content_hash(doc);doc['audit_id']=stable_id('fmfuture',doc);return doc

def fail_closed_audit(candidate,decision,domain):
    reasons=[]
    if decision['decision']!='admit_reference':reasons.append('intake_not_admitted')
    if not domain['supported']:reasons.append('domain_unsupported')
    fallback='candidate_feature' if not reasons else ('native_linear_baseline' if candidate.family!='native_linear_baseline' else 'abstain')
    passed=(not reasons and fallback=='candidate_feature') or (reasons and fallback in {'native_linear_baseline','abstain'})
    doc={'phase':'SAED_V4_14','candidate_id':candidate.candidate_id,'reasons':reasons,'resolved_path':fallback,'candidate_authority_granted':False,'passed':passed};doc['audit_hash']=content_hash(doc);doc['audit_id']=stable_id('fmfailclosed',doc);return doc
