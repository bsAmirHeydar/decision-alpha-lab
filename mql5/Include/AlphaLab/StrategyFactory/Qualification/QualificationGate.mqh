#ifndef ALPHALAB_QUALIFICATION_GATE_MQH
#define ALPHALAB_QUALIFICATION_GATE_MQH
#include "QualificationEnums.mqh"
struct ALQualificationGateResult { string gate_id; ALQualificationStatus status; string reason_code; string evidence_hash; long evaluated_at_ms; };
bool ALGatePassed(const ALQualificationGateResult &gate){ return gate.status==AL_Q_PASS && StringLen(gate.reason_code)==0 && StringLen(gate.evidence_hash)==64; }
#endif
