from __future__ import annotations
from .errors import BudgetError
from .canonical import content_hash
class ResearchLedger:
    MAP={'dataset_episodes':'max_dataset_episodes','training_trials':'max_training_trials','candidate_policies':'max_candidate_policies','ope_evaluations':'max_ope_evaluations','bootstrap_draws':'max_bootstrap_draws','projection_attempts':'max_projection_attempts','synthetic_challenges':'max_synthetic_challenges','failures':'max_failures','hidden_evaluation_queries':'max_hidden_evaluation_queries','protected_evidence_exposures':'protected_evidence_exposure_limit'}
    def __init__(self,contract): self.contract=contract;self.counts={k:0 for k in self.MAP};self.events=[]
    def consume(self,key,n=1,identity=''):
        if key not in self.counts or int(n)<0: raise BudgetError('invalid budget counter')
        nxt=self.counts[key]+int(n);limit=getattr(self.contract,self.MAP[key])
        if nxt>limit: raise BudgetError(f'{key} budget exceeded: {nxt}>{limit}')
        self.counts[key]=nxt;self.events.append({'counter':key,'delta':int(n),'identity':str(identity),'value':nxt});return nxt
    def snapshot(self):
        out={'counts':dict(self.counts),'limits':{v:getattr(self.contract,v) for v in self.MAP.values()},'events':list(self.events)};out['ledger_hash']=content_hash(out);return out
