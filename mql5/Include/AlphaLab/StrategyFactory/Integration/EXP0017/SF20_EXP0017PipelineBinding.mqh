#ifndef __SF20_EXP0017_PIPELINE_BINDING_MQH__
#define __SF20_EXP0017_PIPELINE_BINDING_MQH__
#include "SF20_EXP0017Contracts.mqh"
void SF20_BuildStageEvidence(const string stage,const ENUM_SF20_STAGE_STATUS status,const string input_id,const string output_id,const long known,const string reason,const string detail,SF20_EXP0017StageEvidence &e)
{e.stage=stage;e.status=status;e.input_id=input_id;e.output_id=output_id;e.known_time_utc_msc=known;e.reason_code=reason;e.detail=detail;e.evidence_hash=SF01_StableId("sf20evd",stage+"|"+SF20_StageStatusText(status)+"|"+input_id+"|"+output_id+"|"+IntegerToString(known)+"|"+reason);}
int SF20_BuildFailClosedPilotRoute(const SF01_AnatomyEvent &event,const string context_id,const string candidate_ids,const long known,SF20_EXP0017StageEvidence &out[])
{
 ArrayResize(out,9);SF20_BuildStageEvidence("anatomy",SF20_STAGE_PASSED,event.event_id,event.event_id,known,"CANONICAL_EVENT_VALID","EXP0017 raw divergence mapped",out[0]);
 SF20_BuildStageEvidence("context",context_id!=""?SF20_STAGE_PASSED:SF20_STAGE_GATED,event.event_id,context_id,known,context_id!=""?"CONTEXT_FRAME_BUILT":"CONTEXT_EVIDENCE_ABSENT","shared context boundary",out[1]);
 SF20_BuildStageEvidence("candidate",candidate_ids!=""?SF20_STAGE_PASSED:SF20_STAGE_GATED,context_id,candidate_ids,known,candidate_ids!=""?"CANDIDATE_MATRIX_BUILT":"NO_ADMISSIBLE_CANDIDATE","shared candidate boundary",out[2]);
 SF20_BuildStageEvidence("outcome",candidate_ids!=""?SF20_STAGE_GATED:SF20_STAGE_NOT_RUN,candidate_ids,"",known,candidate_ids!=""?"AWAITING_CAUSAL_PRICE_PATH":"NO_CANDIDATE","research outcome boundary",out[3]);
 SF20_BuildStageEvidence("inference",SF20_STAGE_GATED,context_id,"",known,"NO_GOVERNED_EXP0017_MODEL","reference model substitution forbidden",out[4]);
 SF20_BuildStageEvidence("decision",SF20_STAGE_GATED,"","",known,"INFERENCE_NOT_ACCEPTED","fail closed skip",out[5]);
 SF20_BuildStageEvidence("paper_shadow",SF20_STAGE_GATED,"","",known,"NO_EXECUTION_INTENT","paper broker receives nothing",out[6]);
 SF20_BuildStageEvidence("monitoring",SF20_STAGE_PASSED,event.event_id,SF01_StableId("sf20mon",event.event_id),known,"TELEMETRY_EMITTED","lineage monitoring active",out[7]);
 SF20_BuildStageEvidence("live",SF20_STAGE_GATED,event.event_id,"",known,"LIVE_AUTHORITY_DISABLED","Phase 20 contains no broker authority",out[8]);return ArraySize(out);
}
#endif
