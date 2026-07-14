#ifndef __FP_I09_EVENT_CHAIN_MQH__
#define __FP_I09_EVENT_CHAIN_MQH__
#include "FP_I09_Contracts.mqh"
bool FP_I09_ValidateSequence(FP_I09_LedgerEvent &events[]){ for(int i=0;i<ArraySize(events);i++){ if(events[i].sequence!=i) return false; if(i==0 && events[i].prior_event_hash!="") return false; if(i>0 && events[i].prior_event_hash!=events[i-1].event_hash) return false; } return true; }
#endif
