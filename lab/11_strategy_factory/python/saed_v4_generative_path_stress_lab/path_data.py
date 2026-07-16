from __future__ import annotations
from .canonical import content_hash
from .errors import ContractError
ROW_FIELDS={'timestamp','open','high','low','close','bid','ask','volume','liquidity','regime'}
PATH_FIELDS={'path_id','context_id','start_time','step_seconds','rows','role'}

def validate_real_paths(doc,state_contract,ledger=None):
    if set(doc)!={'dataset_id','context_id','paths','role','known_time_cutoff'}: raise ContractError('real path document fields mismatch')
    if doc['role'] not in {'training','calibration','selection_validation'}: raise ContractError('protected path role')
    if len(doc['paths'])<2: raise ContractError('insufficient real paths')
    out=[]
    for p in doc['paths']:
        if set(p)!=PATH_FIELDS: raise ContractError('real path fields mismatch')
        rows=p['rows']
        if not state_contract.minimum_history<=len(rows)<=state_contract.maximum_history: raise ContractError('history length outside contract')
        for r in rows:
            if set(r)!=ROW_FIELDS: raise ContractError('row fields mismatch')
            if any(k in r for k in state_contract.action_fields_forbidden): raise ContractError('action field contamination')
        out.append(p)
    if ledger: ledger.consume('real_paths',len(out))
    return {'dataset_id':doc['dataset_id'],'context_id':doc['context_id'],'role':doc['role'],'known_time_cutoff':doc['known_time_cutoff'],'path_count':len(out),'dataset_hash':content_hash(doc),'paths':out}

def returns(path):
    cs=[float(r['close']) for r in path['rows']]
    return [(cs[i]/cs[i-1]-1.0) for i in range(1,len(cs))]
def spreads(path): return [(float(r['ask'])-float(r['bid']))/max(float(r['close']),1e-12) for r in path['rows']]
def liquidity(path): return [float(r['liquidity']) for r in path['rows']]
def regimes(path): return [str(r['regime']) for r in path['rows']]
def summary(paths):
    rs=[x for p in paths for x in returns(p)];sp=[x for p in paths for x in spreads(p)];liq=[x for p in paths for x in liquidity(p)];regs=sorted({x for p in paths for x in regimes(p)})
    counts={g:sum(1 for p in paths for x in regimes(p) if x==g) for g in regs};total=sum(counts.values()) or 1
    from .numerics import mean,std,quantile,autocorr
    out={'path_count':len(paths),'step_count':sum(len(p['rows']) for p in paths),'return_mean':mean(rs),'return_std':std(rs),'return_q01':quantile(rs,0.01),'return_q99':quantile(rs,0.99),'return_autocorr_1':autocorr(rs,1),'spread_mean':mean(sp),'liquidity_mean':mean(liq),'regime_occupancy':{g:counts[g]/total for g in regs}}
    out['summary_hash']=content_hash(out);return out
