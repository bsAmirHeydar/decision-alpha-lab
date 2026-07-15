#ifndef ALPHALAB_QUALIFICATION_SECURITY_EVIDENCE_MQH
#define ALPHALAB_QUALIFICATION_SECURITY_EVIDENCE_MQH
struct ALSecurityEvidence { int plaintext_secret_findings; int unsigned_artifacts; int hash_mismatches; bool backup_restore_verified; bool retention_verified; };
bool ALSecurityEvidencePasses(const ALSecurityEvidence &evidence){ return evidence.plaintext_secret_findings==0 && evidence.unsigned_artifacts==0 && evidence.hash_mismatches==0 && evidence.backup_restore_verified && evidence.retention_verified; }
#endif
