from __future__ import annotations
from .canonical import content_hash,stable_id,hash_signed,hash_unit
from .numerics import sigmoid,clamp

def _environment(ordinal,registry):
    for e in registry.environments:
        if e['start_ordinal']<=ordinal<=e['end_ordinal']:return e['environment_id']
    raise ValueError('ordinal outside environment registry')

def build(upstream,v416_dataset,variable_registry,environment_registry,config):
    rows=[]
    for src in v416_dataset['rows']:
        i=src['ordinal'];f=src['features'];env=_environment(i,environment_registry)
        exogenous=hash_signed(f"{config.seed}:z:{src['row_id']}")
        context=0.7*f[0]+0.35*f[1]+0.15*hash_signed(f"ctx:{i}")
        structure=0.55*f[2]+0.25*context+0.12*hash_signed(f"str:{i}")
        liquidity=0.65*f[3]-0.18*context+0.15*hash_signed(f"liq:{i}")
        friction=0.72*f[4]-0.42*liquidity+0.13*hash_signed(f"fr:{i}")
        env_shift={'env_0':-0.15,'env_1':0.05,'env_2':0.18,'env_3':-0.03}[env]
        treatment_score=0.95*exogenous+0.48*context-0.36*friction+env_shift+0.1*hash_signed(f"tr:{i}")
        treatment=1.0 if sigmoid(treatment_score)>0.5 else 0.0
        mediator=0.82*treatment+0.47*liquidity-0.31*friction+0.12*structure+0.11*hash_signed(f"med:{i}")
        outcome=0.88*mediator+0.26*context-0.17*friction+0.09*structure+0.14*hash_signed(f"out:{i}")
        neg_x=hash_signed(f"negx:{config.seed}:{i}")
        neg_y=hash_signed(f"negy:{config.seed+71}:{i}")
        values={'instrument_z':exogenous,'context_state':context,'structure_state':structure,'liquidity_state':liquidity,'execution_friction':friction,'treatment_proxy':treatment,'mediator_fill_quality':mediator,'outcome_proxy':outcome,'negative_control_exposure':neg_x,'negative_control_outcome':neg_y,'environment_code':float(int(env[-1]))}
        row={'row_id':stable_id('v417row',{'source':src['row_id'],'seed':config.seed}),'source_v4_16_row_id':src['row_id'],'ordinal':i,'known_as_of':src['known_as_of'],'environment_id':env,'split':src['split'],'values':{k:float(format(v,'.15g')) for k,v in values.items()},'future_suffix_accessed':False,'synthetic':True,'production_eligible':False}
        row['row_hash']=content_hash(row);rows.append(row)
    out={'phase':'SAED_V4_17','dataset_id':stable_id('v417dataset',{'upstream':upstream['v4_16_dataset_hash'],'rows':len(rows)}),'source_v4_16_dataset_hash':upstream['v4_16_dataset_hash'],'row_count':len(rows),'variable_count':len(variable_registry.variables),'environment_count':len(environment_registry.environments),'rows':rows,'synthetic_only':True,'known_time_ordered':all(a['known_as_of']<=b['known_as_of'] for a,b in zip(rows,rows[1:])),'protected_evidence_exposures':0,'future_suffix_access_count':sum(r['future_suffix_accessed'] for r in rows)}
    out['dataset_hash']=content_hash(out);return out

def ground_truth_graph(variable_registry):
    edges=[('instrument_z','treatment_proxy'),('context_state','structure_state'),('context_state','treatment_proxy'),('context_state','outcome_proxy'),('structure_state','mediator_fill_quality'),('structure_state','outcome_proxy'),('liquidity_state','execution_friction'),('liquidity_state','mediator_fill_quality'),('execution_friction','treatment_proxy'),('execution_friction','mediator_fill_quality'),('execution_friction','outcome_proxy'),('treatment_proxy','mediator_fill_quality'),('mediator_fill_quality','outcome_proxy')]
    out={'phase':'SAED_V4_17','synthetic_benchmark_truth_only':True,'claimable_as_real_mechanism':False,'node_count':len(variable_registry.variables),'edge_count':len(edges),'edges':[{'source':a,'target':b} for a,b in edges]};out['graph_hash']=content_hash(out);return out
