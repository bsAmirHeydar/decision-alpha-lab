#property strict
#include <AlphaLab/StrategyFactory/Operations/OperationsRuntimeLease.mqh>
int OnInit(){ ALOperationsRuntimeLease lease; lease.lease_hash=StringRepeat("a",64); lease.plan_hash=StringRepeat("b",64); lease.environment_hash=StringRepeat("c",64); lease.generation_hash=StringRepeat("d",64); lease.stage=AL_OPS_MICRO_LIVE; lease.max_risk_units=0.1; lease.issued_at_ms=10; lease.expires_at_ms=20; lease.revoked_at_ms=0; if(ALOpsLeaseActive(lease,20)) return INIT_FAILED; Print("UCE-I19 lease expiry self-test passed"); return INIT_SUCCEEDED; }
void OnTick(){}
