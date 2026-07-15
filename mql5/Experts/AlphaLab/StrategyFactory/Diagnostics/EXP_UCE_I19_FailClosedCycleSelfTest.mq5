#property strict
#include <AlphaLab/StrategyFactory/Operations/OperationsCatalog.mqh>
#include <AlphaLab/StrategyFactory/Operations/OperationsCycleAuthorization.mqh>
int OnInit(){ ALOperationsRuntimeLease lease; lease.lease_hash=StringRepeat("a",64); lease.plan_hash=StringRepeat("b",64); lease.environment_hash=StringRepeat("c",64); lease.generation_hash=StringRepeat("d",64); lease.stage=AL_OPS_MICRO_LIVE; lease.max_risk_units=0.1; lease.issued_at_ms=1; lease.expires_at_ms=1000; lease.revoked_at_ms=0; ALOperationsReconciliation r; r.environment_hash=lease.environment_hash; r.generation_hash=lease.generation_hash; r.expected_reservation_hash="x"; r.observed_reservation_hash="y"; ALOperationsCycleAuthorization a=ALOpsAuthorizeCycle(lease,AL_OPS_PASS,r,10,0.1,false); if(a.authority_order||a.decision!=AL_OPS_HALT) return INIT_FAILED; Print("UCE-I19 fail-closed cycle self-test passed; reference authority=",AL_OPERATIONS_ORDER_AUTHORITY); return INIT_SUCCEEDED; }
void OnTick(){}
