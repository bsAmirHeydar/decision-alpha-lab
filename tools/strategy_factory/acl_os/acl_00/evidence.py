from __future__ import annotations
from collections import Counter
from datetime import datetime
from .types import EvidenceRecord, EvidenceClass, Reason, TransitionRequest

# A stronger class can satisfy selected lower-level evidence requirements only
# where the semantics remain valid. Synthetic and estimated evidence never
# substitute for observed/prospective/operational evidence.
SATISFIES={
 EvidenceClass.OBSERVED:{EvidenceClass.OBSERVED},
 EvidenceClass.DERIVED:{EvidenceClass.DERIVED},
 EvidenceClass.ESTIMATED:{EvidenceClass.ESTIMATED},
 EvidenceClass.SYNTHETIC:{EvidenceClass.SYNTHETIC},
 EvidenceClass.PROSPECTIVE:{EvidenceClass.PROSPECTIVE,EvidenceClass.OBSERVED},
 EvidenceClass.OPERATIONAL:{EvidenceClass.OPERATIONAL,EvidenceClass.OBSERVED},
 EvidenceClass.AUTHORIZATION:{EvidenceClass.AUTHORIZATION},
}

class EvidenceEvaluator:
    def evaluate(self,request:TransitionRequest,records:list[EvidenceRecord],requirements:dict,now:datetime)->list[Reason]:
        reasons=[]; by_id={x.evidence_id:x for x in records}
        missing_refs=sorted(set(request.evidence_ids)-set(by_id))
        if missing_refs: reasons.append(Reason("EVIDENCE_REFERENCE_UNRESOLVED",f"Unresolved evidence IDs: {missing_refs}","EVIDENCE_RESOLUTION",False,{"missing":missing_refs}))
        usable=[]
        for ev in records:
            if ev.evidence_id not in request.evidence_ids: continue
            if ev.subject_ref.artifact_id!=request.subject_ref.artifact_id:
                reasons.append(Reason("EVIDENCE_SUBJECT_MISMATCH",f"Evidence {ev.evidence_id} belongs to another subject.","EVIDENCE_SUBJECT_BINDING",False))
                continue
            if not ev.immutable:
                reasons.append(Reason("EVIDENCE_NOT_IMMUTABLE",f"Evidence {ev.evidence_id} is mutable.","EVIDENCE_IMMUTABILITY",False))
                continue
            if ev.known_at>request.requested_at:
                reasons.append(Reason("EVIDENCE_KNOWN_AFTER_REQUEST",f"Evidence {ev.evidence_id} was not known at request time.","EVIDENCE_KNOWN_TIME",False))
                continue
            if ev.known_at<ev.observed_at:
                reasons.append(Reason("INVALID_EVIDENCE_CLOCK",f"Evidence {ev.evidence_id} known_at precedes observed_at.","EVIDENCE_KNOWN_TIME",False))
                continue
            usable.append(ev)
        counts=Counter()
        for ev in usable:
            for satisfied in SATISFIES[ev.evidence_class]: counts[satisfied.value]+=1
        for class_name,min_count in requirements.get("required_classes",{}).items():
            if counts[class_name]<int(min_count):
                reasons.append(Reason("EVIDENCE_CLASS_INSUFFICIENT",f"Need {min_count} {class_name} evidence item(s), found {counts[class_name]}.",f"EVIDENCE_CLASS_{class_name}",bool(requirements.get("waivable",False)),{"required":min_count,"found":counts[class_name],"class":class_name}))
        required_claims=set(requirements.get("required_claims",[])); found_claims={c for ev in usable for c in ev.claims}
        if not required_claims.issubset(found_claims):
            miss=sorted(required_claims-found_claims)
            reasons.append(Reason("EVIDENCE_CLAIM_MISSING",f"Required evidence claims are missing: {miss}","EVIDENCE_REQUIRED_CLAIMS",bool(requirements.get("waivable",False)),{"missing":miss}))
        allowed_env=set(requirements.get("allowed_environments",[]))
        if allowed_env and usable and not any(ev.environment in allowed_env for ev in usable):
            reasons.append(Reason("EVIDENCE_ENVIRONMENT_INELIGIBLE","No evidence came from an eligible environment.","EVIDENCE_ENVIRONMENT",bool(requirements.get("waivable",False)),{"allowed":sorted(allowed_env)}))
        return reasons
