from __future__ import annotations
from .contracts import OpportunityBatch,RankedOpportunity
from .enums import OpportunityStatus
from .canonical import canonical_sha256

def rank_batch(batch:OpportunityBatch, as_of_ms:int|None=None, max_ece:float=0.15):
    now=batch.as_of_ms if as_of_ms is None else as_of_ms
    ranked=[]
    for c in batch.candidates:
        reasons=[];status=OpportunityStatus.ELIGIBLE
        if c.expires_at_ms<=now: reasons.append('expired');status=OpportunityStatus.REJECTED
        if c.calibration.expected_calibration_error>max_ece: reasons.append('calibration_too_weak');status=OpportunityStatus.REJECTED
        if c.liquidity_score<=0: reasons.append('no_liquidity');status=OpportunityStatus.REJECTED
        risk_den=max(c.expected_loss+c.uncertainty+c.turnover_cost,1e-12)
        calibration_factor=max(0.0,1.0-c.calibration.expected_calibration_error)
        novelty_factor=0.5+0.5*c.novelty
        score=(c.expected_return+c.utility_mean)*calibration_factor*novelty_factor*c.liquidity_score/risk_den
        ranked.append(RankedOpportunity(c,score,status,tuple(sorted(set(reasons)))))
    return tuple(sorted(ranked,key=lambda x:(x.status is not OpportunityStatus.ELIGIBLE,-x.score,x.candidate.candidate_id)))

def queue_hash(ranked): return canonical_sha256(ranked)
