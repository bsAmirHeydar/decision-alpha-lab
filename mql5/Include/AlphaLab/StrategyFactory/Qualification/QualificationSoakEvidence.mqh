#ifndef ALPHALAB_QUALIFICATION_SOAK_EVIDENCE_MQH
#define ALPHALAB_QUALIFICATION_SOAK_EVIDENCE_MQH
struct ALSoakEvidence { int duration_minutes; long processed_events; int critical_errors; int unhandled_exceptions; int reconciliation_mismatches; int duplicate_actions; int stale_actions; double memory_growth_mb; double p99_latency_ms; };
bool ALSoakEvidencePasses(const ALSoakEvidence &evidence,const int min_minutes,const long min_events,const double max_memory_mb,const double max_p99_ms){ return evidence.duration_minutes>=min_minutes && evidence.processed_events>=min_events && evidence.critical_errors==0 && evidence.unhandled_exceptions==0 && evidence.reconciliation_mismatches==0 && evidence.duplicate_actions==0 && evidence.stale_actions==0 && evidence.memory_growth_mb<=max_memory_mb && evidence.p99_latency_ms<=max_p99_ms; }
#endif
