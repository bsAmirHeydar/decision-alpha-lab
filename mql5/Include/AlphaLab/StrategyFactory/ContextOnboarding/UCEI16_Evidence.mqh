#ifndef ALPHALAB_UCEI16_EVIDENCE_MQH
#define ALPHALAB_UCEI16_EVIDENCE_MQH
struct UCEI16_EvidenceBundle { string bundle_id; string manifest_hash; string invariance_hash; string test_evidence_hash; int parity_report_count; int migration_report_count; };
bool UCEI16_ValidateEvidence(const UCEI16_EvidenceBundle &b){ return StringLen(b.bundle_id)>0 && StringLen(b.manifest_hash)==64 && StringLen(b.invariance_hash)==64 && StringLen(b.test_evidence_hash)==64 && b.parity_report_count>0 && b.migration_report_count==3; }
#endif
