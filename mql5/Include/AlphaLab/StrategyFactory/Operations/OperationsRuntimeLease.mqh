#ifndef ALPHALAB_OPERATIONS_RUNTIME_LEASE_MQH
#define ALPHALAB_OPERATIONS_RUNTIME_LEASE_MQH
#include "OperationsEnums.mqh"
#include "OperationsHashGuard.mqh"
struct ALOperationsRuntimeLease { string lease_hash; string plan_hash; string environment_hash; string generation_hash; ALOperationsStage stage; double max_risk_units; long issued_at_ms; long expires_at_ms; long revoked_at_ms; };
bool ALOpsLeaseActive(const ALOperationsRuntimeLease &lease,const long now_ms){ return ALOpsIsSha256(lease.lease_hash)&&ALOpsIsSha256(lease.plan_hash)&&ALOpsIsSha256(lease.environment_hash)&&ALOpsIsSha256(lease.generation_hash)&&lease.max_risk_units>=0.0&&lease.issued_at_ms<=now_ms&&now_ms<lease.expires_at_ms&&lease.revoked_at_ms==0; }
#endif
