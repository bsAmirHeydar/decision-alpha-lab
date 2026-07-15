#ifndef __DECISION_ALPHA_LAB_SAED_V4_11_HANDOFF_MQH__
#define __DECISION_ALPHA_LAB_SAED_V4_11_HANDOFF_MQH__
#include "SAEDV411Contracts.mqh"
#include "SAEDV411Canonical.mqh"
bool SAEDV411ValidateHandoff(const SAEDV411HandoffContract &handoff)
{
   if(handoff.next_phase!="SAED_V4_12") return false;
   if(!SAEDV411IsSha256(handoff.handoff_hash)) return false;
   if(!SAEDV411IsSha256(handoff.encoder_checkpoint_hash)) return false;
   if(!handoff.outcome_supervision_absent || !handoff.future_suffix_forbidden) return false;
   if(handoff.send_order) return false;
   return true;
}
#endif
