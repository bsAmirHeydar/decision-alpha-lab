#ifndef ALPHALAB_OPERATIONS_TELEMETRY_MQH
#define ALPHALAB_OPERATIONS_TELEMETRY_MQH
#include "OperationsHashGuard.mqh"
struct ALOperationsTelemetry { string environment_hash; string generation_hash; long captured_at_ms; long last_heartbeat_ms; long feature_age_ms; double p99_latency_ms; int queue_depth; double memory_growth_mb; bool broker_connected; bool history_synchronized; int open_positions; double open_risk; double reserved_risk; double daily_pnl; double weekly_pnl; double reject_rate; double drift_score; int duplicate_actions; int stale_actions; int unreserved_actions; int critical_errors; };
bool ALOpsTelemetryShapeValid(const ALOperationsTelemetry &value){ return ALOpsIsSha256(value.environment_hash)&&ALOpsIsSha256(value.generation_hash)&&value.last_heartbeat_ms<=value.captured_at_ms&&value.feature_age_ms>=0&&value.p99_latency_ms>=0.0&&value.queue_depth>=0&&value.memory_growth_mb>=0.0&&value.open_positions>=0&&value.open_risk>=0.0&&value.reserved_risk>=0.0&&value.reject_rate>=0.0&&value.reject_rate<=1.0&&value.drift_score>=0.0&&value.duplicate_actions>=0&&value.stale_actions>=0&&value.unreserved_actions>=0&&value.critical_errors>=0; }
#endif
