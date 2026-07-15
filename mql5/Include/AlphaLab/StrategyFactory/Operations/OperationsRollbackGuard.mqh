#ifndef ALPHALAB_OPERATIONS_ROLLBACK_GUARD_MQH
#define ALPHALAB_OPERATIONS_ROLLBACK_GUARD_MQH
#include "OperationsHashGuard.mqh"
struct ALOperationsRollbackEvidence { string from_generation_hash; string to_generation_hash; long initiated_at_ms; long completed_at_ms; double max_allowed_seconds; bool orders_blocked; bool positions_reconciled; bool reservations_reconciled; bool target_generation_active; };
bool ALOpsRollbackPasses(const ALOperationsRollbackEvidence &r){ if(!ALOpsIsSha256(r.from_generation_hash)||!ALOpsIsSha256(r.to_generation_hash)||r.completed_at_ms<r.initiated_at_ms||r.max_allowed_seconds<=0.0) return false; double seconds=(double)(r.completed_at_ms-r.initiated_at_ms)/1000.0; return seconds<=r.max_allowed_seconds&&r.orders_blocked&&r.positions_reconciled&&r.reservations_reconciled&&r.target_generation_active; }
#endif
