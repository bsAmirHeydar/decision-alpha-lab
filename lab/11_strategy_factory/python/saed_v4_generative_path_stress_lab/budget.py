from __future__ import annotations
from .errors import BudgetError
from .canonical import content_hash
class BudgetLedger:
    MAP={'real_paths':'max_real_paths','generated_paths':'max_generated_paths','stress_paths':'max_stress_paths','generator_trials':'max_generator_trials','adversarial_steps':'max_adversarial_steps','fidelity_evaluations':'max_fidelity_evaluations','failures':'max_failures','hidden_evaluation_queries':'max_hidden_evaluation_queries','protected_evidence_exposures':'protected_evidence_exposure_limit'}
    def __init__(self,contract):
        self.contract=contract;self.counts={k:0 for k in self.MAP}
    def consume(self,key,n=1):
        if key not in self.counts or int(n)<0: raise BudgetError('invalid budget counter')
        nxt=self.counts[key]+int(n);limit=getattr(self.contract,self.MAP[key])
        if nxt>limit: raise BudgetError(f'{key} budget exceeded: {nxt}>{limit}')
        self.counts[key]=nxt;return nxt
    def snapshot(self):
        out=dict(self.counts);out['limits']={v:getattr(self.contract,v) for v in self.MAP.values()};out['ledger_hash']=content_hash(out);return out
