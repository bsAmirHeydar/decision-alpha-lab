from __future__ import annotations
from .types import Reason,TransitionRequest

ORDER=["REFERENCE_ONLY","DIAGNOSTIC","RESEARCH_TRIAGE","STATISTICAL_ELIGIBILITY","PAPER_EVIDENCE","SHADOW_EVIDENCE","MICRO_LIVE_EVIDENCE","SIGNED_AUTHORIZATION_REQUIRED"]

class ClaimCeilingEvaluator:
    def evaluate(self,request:TransitionRequest,policy:dict)->list[Reason]:
        ceiling=policy.get("claim_ceiling","REFERENCE_ONLY")
        try: req_i=ORDER.index(request.claim_requested); ceil_i=ORDER.index(ceiling)
        except ValueError: return [Reason("UNKNOWN_CLAIM_CEILING","Unknown claim ceiling.","CLAIM_CEILING_CATALOG",False)]
        if req_i>ceil_i:
            return [Reason("CLAIM_CEILING_EXCEEDED",f"Requested claim {request.claim_requested} exceeds {ceiling}.","CLAIM_CEILING",False,{"requested":request.claim_requested,"ceiling":ceiling})]
        return []
