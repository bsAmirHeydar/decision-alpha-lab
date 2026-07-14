from __future__ import annotations
from collections import defaultdict
from .models import LatentHypothesis,HypothesisAssessment,HypothesisState
from .enums import HypothesisStatus
from .errors import ContractError,IdentityError

class HypothesisLedger:
    def __init__(self,hypotheses=()):self.hypotheses={x.hypothesis_id:x for x in hypotheses};self.assessments=[];self.ids=set()
    def append(self,a:HypothesisAssessment):
        if a.hypothesis_id not in self.hypotheses:raise ContractError('unknown hypothesis')
        if not (-1<=a.score<=1):raise ContractError('score out of range')
        if not (0<a.weight<=1):raise ContractError('weight out of range')
        if not a.evidence_hash or len(a.evidence_hash)!=64:raise ContractError('evidence hash required')
        if a.assessment_id in self.ids:return a.assessment_id
        self.assessments.append(a);self.ids.add(a.assessment_id);return a.assessment_id
    def state(self,hypothesis_id:str)->HypothesisState:
        h=self.hypotheses[hypothesis_id];xs=[a for a in self.assessments if a.hypothesis_id==hypothesis_id]
        total=sum(a.weight for a in xs)
        score=(h.prior_weight+sum(a.score*a.weight for a in xs))/(1+total)
        if not xs:status=HypothesisStatus.DECLARED
        elif score>=0.35:status=HypothesisStatus.SUPPORTED
        elif score<=-0.35:status=HypothesisStatus.REJECTED
        elif any(a.score<0 for a in xs):status=HypothesisStatus.CHALLENGED
        else:status=HypothesisStatus.UNRESOLVED
        return HypothesisState(hypothesis_id,round(score,12),round(total,12),status,tuple(sorted(a.assessment_id for a in xs)))
    def states(self):return tuple(self.state(k) for k in sorted(self.hypotheses))
