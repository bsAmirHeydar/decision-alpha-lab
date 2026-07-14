#ifndef FP_I15_PAPER_QUOTA_MQH
#define FP_I15_PAPER_QUOTA_MQH
#include "FP_I15_Contracts.mqh"
#include "FP_I15_Hash.mqh"
#include "FP_I15_Policy.mqh"
bool FP_I15_ReserveQuota(const FP_I15_Plan &plan,const FP_I15_POLICY_PROFILE policy,FP_I15_QuotaRecord &q){ if(policy==FP_I15_POLICY_UNSET)return false; if(q.state==FP_I15_QUOTA_RESERVED||q.state==FP_I15_QUOTA_CONSUMED)return q.winner_signal_id==plan.signal_id; q.quota_key_id=plan.quota_key_id;q.state=FP_I15_QUOTA_RESERVED;q.winner_signal_id=plan.signal_id;q.plan_id=plan.plan_id;q.generation++;q.reservation_id=FP_I15_Id("FPPRES",q.quota_key_id+plan.signal_id+IntegerToString(q.generation));q.consumed_event=FP_I15_CONSUME_UNSET; if(FP_I15_PolicyConsumeEvent(policy)==FP_I15_CONSUME_PLAN){q.state=FP_I15_QUOTA_CONSUMED;q.consumed_event=FP_I15_CONSUME_PLAN;}return true; }
void FP_I15_TriggerQuota(FP_I15_QuotaRecord &q,const FP_I15_POLICY_PROFILE policy,const FP_I15_CONSUME_EVENT event){ if(q.state==FP_I15_QUOTA_RESERVED && FP_I15_PolicyConsumeEvent(policy)==event){q.state=FP_I15_QUOTA_CONSUMED;q.consumed_event=event;} }
#endif
