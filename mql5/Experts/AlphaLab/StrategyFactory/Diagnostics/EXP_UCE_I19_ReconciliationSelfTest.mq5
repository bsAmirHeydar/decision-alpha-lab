#property strict
#include <AlphaLab/StrategyFactory/Operations/OperationsReconciliationGuard.mqh>
int OnInit(){ ALOperationsReconciliation r; r.environment_hash=StringRepeat("a",64); r.generation_hash=StringRepeat("b",64); r.expected_reservation_hash="r"; r.observed_reservation_hash="r"; r.expected_order_hash="o"; r.observed_order_hash="o"; r.expected_position_hash="p"; r.observed_position_hash="p"; r.orphan_orders=0; r.orphan_positions=0; r.missing_orders=0; r.missing_positions=0; r.duplicate_intents=0; r.unreserved_positions=0; if(!ALOpsReconciliationExact(r)) return INIT_FAILED; r.unreserved_positions=1; if(ALOpsReconciliationExact(r)) return INIT_FAILED; Print("UCE-I19 reconciliation self-test passed"); return INIT_SUCCEEDED; }
void OnTick(){}
