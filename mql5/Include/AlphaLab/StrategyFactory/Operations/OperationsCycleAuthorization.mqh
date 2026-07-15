#ifndef ALPHALAB_OPERATIONS_CYCLE_AUTHORIZATION_MQH
#define ALPHALAB_OPERATIONS_CYCLE_AUTHORIZATION_MQH
#include "OperationsEnums.mqh"
#include "OperationsRuntimeLease.mqh"
#include "OperationsHealthGate.mqh"
#include "OperationsReconciliationGuard.mqh"
struct ALOperationsCycleAuthorization { ALOperationsDecision decision; bool authority_order; double max_incremental_risk; string reason_code; };
ALOperationsCycleAuthorization ALOpsAuthorizeCycle(const ALOperationsRuntimeLease &lease,const ALOperationsStatus health,const ALOperationsReconciliation &reconciliation,const long now_ms,const double risk_headroom,const bool manual_kill){ ALOperationsCycleAuthorization result; result.decision=AL_OPS_HALT; result.authority_order=false; result.max_incremental_risk=0.0; result.reason_code="fail_closed"; if(manual_kill) { result.reason_code="manual_kill"; return result; } if(!ALOpsLeaseActive(lease,now_ms)){ result.reason_code="lease_inactive"; return result; } if(health==AL_OPS_FAIL){ result.reason_code="health_failed"; return result; } if(!ALOpsReconciliationExact(reconciliation)){ result.reason_code="reconciliation_failed"; return result; } if(lease.stage<=AL_OPS_SHADOW){ result.decision=AL_OPS_ALLOW_NO_SEND; result.reason_code=""; return result; } if(health==AL_OPS_DEGRADED){ result.decision=AL_OPS_DERISK; result.reason_code="health_degraded"; return result; } result.max_incremental_risk=MathMin(lease.max_risk_units,risk_headroom); if(result.max_incremental_risk<=0.0){ result.decision=AL_OPS_HOLD; result.reason_code="zero_risk_headroom"; return result; } result.decision=AL_OPS_ALLOW_BOUNDED; result.authority_order=true; result.reason_code=""; return result; }
#endif
