#ifndef ALPHALAB_OPERATIONS_RAMP_GATE_MQH
#define ALPHALAB_OPERATIONS_RAMP_GATE_MQH
#include "OperationsEnums.mqh"
struct ALOperationsProspectiveWindow { ALOperationsStage stage; int sessions; int events; int calendar_days; int reconciliation_failures; int high_incidents; int critical_incidents; int policy_breaches; double reject_rate; double p99_latency_ms; double drift_score; };
bool ALOpsAdjacentRamp(const ALOperationsStage current_stage,const ALOperationsStage requested_stage){ return requested_stage==current_stage+1 && current_stage>=AL_OPS_PAPER && current_stage<AL_OPS_PRODUCTION; }
bool ALOpsRampEligibleForHumanReview(const ALOperationsProspectiveWindow &w,const ALOperationsStage requested_stage,const int min_sessions,const int min_events,const int min_days,const double max_reject_rate,const double max_latency,const double max_drift){ return ALOpsAdjacentRamp(w.stage,requested_stage)&&w.sessions>=min_sessions&&w.events>=min_events&&w.calendar_days>=min_days&&w.reconciliation_failures==0&&w.high_incidents==0&&w.critical_incidents==0&&w.policy_breaches==0&&w.reject_rate<=max_reject_rate&&w.p99_latency_ms<=max_latency&&w.drift_score<=max_drift; }
#endif
