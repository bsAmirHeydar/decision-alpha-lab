#ifndef ALPHALAB_QUALIFICATION_COMPILE_EVIDENCE_MQH
#define ALPHALAB_QUALIFICATION_COMPILE_EVIDENCE_MQH
struct ALCompileEvidence { string target; string source_hash; string log_hash; string output_hash; int exit_code; int errors; int warnings; };
bool ALCompileEvidencePasses(const ALCompileEvidence &evidence,const int max_warnings){ return evidence.exit_code==0 && evidence.errors==0 && evidence.warnings<=max_warnings && StringLen(evidence.source_hash)==64 && StringLen(evidence.log_hash)==64 && StringLen(evidence.output_hash)==64; }
#endif
