from __future__ import annotations
from .contracts import FidelityContract
from .path_data import summary
from .numerics import l1
from .canonical import content_hash

def compare(real_paths,synthetic_paths,contract_mapping,ledger=None):
    c=FidelityContract.from_mapping(contract_mapping);a=summary(real_paths);b=summary(synthetic_paths)
    regs=sorted(set(a['regime_occupancy'])|set(b['regime_occupancy']));occ=l1([a['regime_occupancy'].get(g,0) for g in regs],[b['regime_occupancy'].get(g,0) for g in regs])
    metrics={'return_mean_error':abs(a['return_mean']-b['return_mean']),'return_std_error':abs(a['return_std']-b['return_std']),'tail_quantile_error':max(abs(a['return_q01']-b['return_q01']),abs(a['return_q99']-b['return_q99'])),'autocorrelation_error':abs(a['return_autocorr_1']-b['return_autocorr_1']),'spread_error':abs(a['spread_mean']-b['spread_mean']),'liquidity_error':abs(a['liquidity_mean']-b['liquidity_mean']),'regime_occupancy_l1':occ}
    scales={'return_mean_error':c.maximum_return_mean_error,'return_std_error':c.maximum_return_std_error,'tail_quantile_error':c.maximum_tail_quantile_error,'autocorrelation_error':c.maximum_autocorrelation_error,'spread_error':c.maximum_spread_error,'liquidity_error':c.maximum_liquidity_error,'regime_occupancy_l1':c.maximum_regime_occupancy_l1}
    normalized={k:metrics[k]/max(scales[k],1e-12) for k in metrics};composite=sum(normalized.values())/len(normalized);dist=min(1.0,composite/(1+composite));passed=all(metrics[k]<=scales[k] for k in metrics) and composite<=c.maximum_composite_distance and dist<=c.maximum_distinguishability_proxy
    if ledger:ledger.consume('fidelity_evaluations',1)
    out={'real_summary':a,'synthetic_summary':b,'metrics':metrics,'thresholds':scales,'normalized_errors':normalized,'composite_distance':composite,'distinguishability_proxy':dist,'passed':passed,'stress_only_usable':True,'positive_evidence_usable':False};out['fidelity_report_hash']=content_hash(out);return out
