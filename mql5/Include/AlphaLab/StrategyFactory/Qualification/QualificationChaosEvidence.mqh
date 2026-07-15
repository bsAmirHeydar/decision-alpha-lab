#ifndef ALPHALAB_QUALIFICATION_CHAOS_EVIDENCE_MQH
#define ALPHALAB_QUALIFICATION_CHAOS_EVIDENCE_MQH
struct ALChaosEvidence { string scenario_id; bool detected; bool fail_closed; bool recovered; bool emitted_unreserved_action; int duplicate_actions; double recovery_seconds; };
bool ALChaosEvidencePasses(const ALChaosEvidence &evidence,const double max_recovery_seconds){ return evidence.detected && evidence.fail_closed && evidence.recovered && !evidence.emitted_unreserved_action && evidence.duplicate_actions==0 && evidence.recovery_seconds<=max_recovery_seconds; }
#endif
