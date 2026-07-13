#property strict
#property version "1.00"
input int InpBrokerUtcOffsetMinutes=0;
#include <FaerieProtocol/EXP0019/Time/FP_I03_All.mqh>
int OnInit()
  {
   FP_I03_TimeKernelConfig config;FP_I03_DefaultConfig(config);datetime broker_now=TimeCurrent();datetime utc_now=0;string reason="";
   if(!FP_I03_BrokerToUtc(broker_now,InpBrokerUtcOffsetMinutes,utc_now,reason)){Print("FP-I03 BLOCKED ",reason);return INIT_FAILED;}
   FP_I03_CalendarSnapshot snapshot;if(!FP_I03_BuildSnapshot(utc_now,config,snapshot,reason)){Print("FP-I03 BLOCKED ",reason);return INIT_FAILED;}
   Print(FP_I03_DiagnosticLine(snapshot));return INIT_SUCCEEDED;
  }
void OnTick(){}
