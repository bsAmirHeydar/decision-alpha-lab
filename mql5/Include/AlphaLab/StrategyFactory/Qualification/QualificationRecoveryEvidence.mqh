#ifndef ALPHALAB_QUALIFICATION_RECOVERY_EVIDENCE_MQH
#define ALPHALAB_QUALIFICATION_RECOVERY_EVIDENCE_MQH
struct ALRecoveryEvidence { string expected_ledger_hash; string observed_ledger_hash; int duplicate_actions; int unreserved_actions; int state_divergences; double rto_seconds; double rpo_seconds; bool kill_switch_verified; bool rollback_verified; };
bool ALRecoveryEvidencePasses(const ALRecoveryEvidence &evidence,const double max_rto,const double max_rpo){ return evidence.expected_ledger_hash==evidence.observed_ledger_hash && evidence.duplicate_actions==0 && evidence.unreserved_actions==0 && evidence.state_divergences==0 && evidence.rto_seconds<=max_rto && evidence.rpo_seconds<=max_rpo && evidence.kill_switch_verified && evidence.rollback_verified; }
#endif
