from __future__ import annotations
from .contracts import ScenarioContract,AmbiguitySetContract
from .errors import ScenarioError
from .canonical import content_hash
from .numerics import normalize

FORBIDDEN_KEYS={'future_suffix','future_outcome','protected_final_evidence','hidden_evaluation_label','live_credential'}

def _scan(v):
    if isinstance(v,dict):
        bad=FORBIDDEN_KEYS & set(v)
        if bad: raise ScenarioError(f'forbidden scenario input: {sorted(bad)}')
        for x in v.values(): _scan(x)
    elif isinstance(v,list):
        for x in v:_scan(x)

def compile_scenarios(score_table,scenario_mapping,ambiguity_mapping,ledger=None):
    _scan(score_table)
    sc=ScenarioContract.from_mapping(scenario_mapping);ac=AmbiguitySetContract.from_mapping(ambiguity_mapping)
    rows={r['treatment_id']:r for r in score_table['rows']};tids=sorted(rows)
    if ledger: ledger.consume('candidates',len(tids))
    native=[]
    for name in sc.native_scenarios:
        utils={tid:float(rows[tid].get('scenario_utilities',{}).get(name,rows[tid]['mean_utility'])) for tid in tids}
        native.append({'scenario_id':f'native::{name}','family':'native','weight':1.0,'utilities':utils,'shocks':{}})
    scenarios=list(native)
    axes=set(sc.shock_axes)
    def add(sid,family,transform,shocks):
        if len(scenarios)>=sc.max_scenarios:return
        utils={tid:float(transform(tid,rows[tid])) for tid in tids}
        scenarios.append({'scenario_id':sid,'family':family,'weight':1.0,'utilities':utils,'shocks':shocks})
    base=lambda r:float(r['mean_utility'])
    if 'cost' in axes:add('shock::cost_up','cost',lambda t,r:base(r)-ac.cost_shock_bound*(1+float(r['complexity'])/5),{'cost':ac.cost_shock_bound})
    if 'tail' in axes:add('shock::tail_down','tail',lambda t,r:base(r)-ac.tail_shock_bound*(1+abs(min(0.0,float(r['tail_cvar'])))),{'tail':ac.tail_shock_bound})
    if 'support' in axes:add('shock::support_loss','support',lambda t,r:base(r)-ac.support_shock_bound*(0.25+float(r['utility_std'])),{'support':ac.support_shock_bound})
    if 'latency' in axes:add('shock::latency','latency',lambda t,r:base(r)-0.035*(1+float(r['complexity'])/3),{'latency':0.035})
    if 'calibration' in axes:add('shock::calibration_down','calibration',lambda t,r:float(r['lower_confidence_utility'])-ac.mean_shift_bound,{'mean_shift':ac.mean_shift_bound})
    if sc.include_joint_adverse:add('shock::joint_adverse','joint',lambda t,r:min(float(r['cvar_utility']),float(r['lower_confidence_utility']))-ac.cost_shock_bound-ac.tail_shock_bound-ac.mean_shift_bound,{'cost':ac.cost_shock_bound,'tail':ac.tail_shock_bound,'mean_shift':ac.mean_shift_bound})
    if sc.include_benign_control:add('control::benign','benign',lambda t,r:float(r['upper_confidence_utility'])+0.5*ac.mean_shift_bound,{'mean_shift':-0.5*ac.mean_shift_bound})
    scenarios=scenarios[:sc.max_scenarios]
    ws=normalize([s['weight'] for s in scenarios],ac.probability_floor)
    for s,p in zip(scenarios,ws):s['nominal_probability']=p
    if ledger: ledger.consume('scenarios',len(scenarios))
    out={'context_id':score_table['context_id'],'treatments':tids,'scenarios':scenarios,'scenario_count':len(scenarios),'future_suffix_used':False,'protected_evidence_used':False,'deterministic':True}
    out['scenario_set_hash']=content_hash(out);return out

def future_suffix_invariance(score_table,mutated,scenario_mapping,ambiguity_mapping):
    a=compile_scenarios(score_table,scenario_mapping,ambiguity_mapping)
    safe=dict(mutated);safe.pop('future_suffix',None);safe.pop('future_outcome',None);safe.pop('protected_final_evidence',None)
    b=compile_scenarios(safe,scenario_mapping,ambiguity_mapping)
    return {'passed':a['scenario_set_hash']==b['scenario_set_hash'],'original_hash':a['scenario_set_hash'],'mutated_hash':b['scenario_set_hash'],'future_suffix_ignored':True}
