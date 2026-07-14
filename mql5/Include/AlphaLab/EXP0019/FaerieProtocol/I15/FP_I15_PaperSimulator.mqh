#ifndef FP_I15_PAPER_SIMULATOR_MQH
#define FP_I15_PAPER_SIMULATOR_MQH
#include "FP_I15_OrderLifecycle.mqh"
#include "FP_I15_PaperQuota.mqh"
bool FP_I15_SimulateImmediateFill(const FP_I15_Plan &plan,const FP_I15_POLICY_PROFILE policy,FP_I15_QuotaRecord &quota,FP_I15_PaperOrder &order){ if(!FP_I15_ReserveQuota(plan,policy,quota))return false; order.order_id=FP_I15_Id("FPORD",plan.plan_id);order.plan_id=plan.plan_id;order.state=FP_I15_ORDER_CREATED;order.requested_volume=plan.sizing.volume;order.filled_volume=0;order.average_fill_price=0; if(!FP_I15_OrderTransition(order,FP_I15_ORDER_VALIDATED))return false; if(!FP_I15_OrderTransition(order,FP_I15_ORDER_ATTEMPTED))return false; FP_I15_TriggerQuota(quota,policy,FP_I15_CONSUME_ATTEMPT); if(!FP_I15_OrderTransition(order,FP_I15_ORDER_ACCEPTED))return false; FP_I15_TriggerQuota(quota,policy,FP_I15_CONSUME_ACCEPTED); if(!FP_I15_OrderTransition(order,FP_I15_ORDER_FILLED))return false; order.filled_volume=order.requested_volume;order.average_fill_price=plan.geometry.entry;FP_I15_TriggerQuota(quota,policy,FP_I15_CONSUME_FIRST_FILL);return true; }
#endif
