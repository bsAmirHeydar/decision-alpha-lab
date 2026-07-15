#ifndef ALPHALAB_OPERATIONS_RECONCILIATION_GUARD_MQH
#define ALPHALAB_OPERATIONS_RECONCILIATION_GUARD_MQH
#include "OperationsHashGuard.mqh"
struct ALOperationsReconciliation { string environment_hash; string generation_hash; string expected_reservation_hash; string observed_reservation_hash; string expected_order_hash; string observed_order_hash; string expected_position_hash; string observed_position_hash; int orphan_orders; int orphan_positions; int missing_orders; int missing_positions; int duplicate_intents; int unreserved_positions; long reconciled_at_ms; };
bool ALOpsReconciliationExact(const ALOperationsReconciliation &r){ if(!ALOpsIsSha256(r.environment_hash)||!ALOpsIsSha256(r.generation_hash)) return false; return r.expected_reservation_hash==r.observed_reservation_hash&&r.expected_order_hash==r.observed_order_hash&&r.expected_position_hash==r.observed_position_hash&&r.orphan_orders==0&&r.orphan_positions==0&&r.missing_orders==0&&r.missing_positions==0&&r.duplicate_intents==0&&r.unreserved_positions==0; }
#endif
