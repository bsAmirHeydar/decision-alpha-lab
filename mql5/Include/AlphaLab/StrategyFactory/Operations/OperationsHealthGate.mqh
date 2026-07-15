#ifndef ALPHALAB_OPERATIONS_HEALTH_GATE_MQH
#define ALPHALAB_OPERATIONS_HEALTH_GATE_MQH
#include "OperationsEnums.mqh"
#include "OperationsTelemetry.mqh"
#include "OperationsRiskEnvelope.mqh"
struct ALOperationsHealthPolicy { long heartbeat_timeout_ms; long max_feature_age_ms; double max_p99_latency_ms; int max_queue_depth; double max_memory_growth_mb; double max_reject_rate; double max_drift_score; };
ALOperationsStatus ALOpsEvaluateHealth(const ALOperationsTelemetry &t,const ALOperationsHealthPolicy &p,const ALOperationsRiskEnvelope &r,const long now_ms){ if(!ALOpsTelemetryShapeValid(t)||!ALOpsRiskEnvelopeValid(r)) return AL_OPS_FAIL; if(t.captured_at_ms>now_ms||now_ms-t.last_heartbeat_ms>p.heartbeat_timeout_ms||t.feature_age_ms>p.max_feature_age_ms||!t.broker_connected||!t.history_synchronized||t.unreserved_actions>0||t.duplicate_actions>0||t.stale_actions>0||t.critical_errors>0||t.open_risk>r.max_open_risk||t.reserved_risk>r.max_total_risk||-t.daily_pnl>r.max_daily_loss||-t.weekly_pnl>r.max_weekly_loss||t.open_positions>r.max_positions) return AL_OPS_FAIL; if(t.p99_latency_ms>p.max_p99_latency_ms||t.queue_depth>p.max_queue_depth||t.memory_growth_mb>p.max_memory_growth_mb||t.reject_rate>p.max_reject_rate||t.drift_score>p.max_drift_score) return AL_OPS_DEGRADED; return AL_OPS_PASS; }
#endif
