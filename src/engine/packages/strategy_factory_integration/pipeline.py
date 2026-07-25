from __future__ import annotations
from .enums import StageStatus
from .hashing import stable_id
from .models import CanonicalAnatomyEvent, StageEvidence

STAGES=("anatomy","context","candidate","outcome","inference","decision","paper_shadow","monitoring","live")

class PilotPipelineGate:
    """Evidence-only pilot route. It never fabricates a trained EXP0017 model or a live intent."""
    def route(self,event:CanonicalAnatomyEvent,known_time_ms:int,context_id:str="",candidate_ids:tuple[str,...]=())->tuple[StageEvidence,...]:
        evidence=[]
        def add(stage,status,input_id,output_id,reason,detail):
            evidence.append(StageEvidence(stage,status,input_id,output_id,known_time_ms,reason,detail))
        add("anatomy",StageStatus.PASSED,event.event_id,event.event_id,"CANONICAL_EVENT_VALID","EXP0017 candidate mapped with causal known time")
        if context_id:
            add("context",StageStatus.PASSED,event.event_id,context_id,"CONTEXT_FRAME_BUILT","shared context engine accepted the event")
        else:
            add("context",StageStatus.GATED,event.event_id,"","CONTEXT_EVIDENCE_ABSENT","pilot caller did not supply context evidence")
        if candidate_ids:
            add("candidate",StageStatus.PASSED,context_id,"|".join(candidate_ids),"CANDIDATE_MATRIX_BUILT","shared candidate matrix produced research candidates")
            add("outcome",StageStatus.GATED,candidate_ids[0],"","AWAITING_CAUSAL_PRICE_PATH","outcome engine requires subsequent observations")
        else:
            add("candidate",StageStatus.GATED,context_id,"","NO_ADMISSIBLE_CANDIDATE","no candidate forwarded")
            add("outcome",StageStatus.NOT_RUN,"","","NO_CANDIDATE","outcome route not invoked")
        add("inference",StageStatus.GATED,context_id,"","NO_GOVERNED_EXP0017_MODEL","reference models cannot be substituted")
        add("decision",StageStatus.GATED,"","","INFERENCE_NOT_ACCEPTED","fail-closed skip")
        add("paper_shadow",StageStatus.GATED,"","","NO_EXECUTION_INTENT","paper broker receives nothing")
        add("monitoring",StageStatus.PASSED,event.event_id,stable_id("sf20mon",event.event_id),"TELEMETRY_EMITTED","pilot telemetry and lineage recorded")
        add("live",StageStatus.GATED,event.event_id,"","LIVE_AUTHORITY_DISABLED","Phase 20 contains no broker authority")
        return tuple(evidence)
