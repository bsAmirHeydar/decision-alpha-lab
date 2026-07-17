#ifndef SAED_V4_39_RECONCILIATION_MQH
#define SAED_V4_39_RECONCILIATION_MQH
struct SAEDV439ReconciliationRecord { string intent_id; bool reconciled; long live_order_id; long live_fill_id; double cash_delta; double position_delta; };
#endif
