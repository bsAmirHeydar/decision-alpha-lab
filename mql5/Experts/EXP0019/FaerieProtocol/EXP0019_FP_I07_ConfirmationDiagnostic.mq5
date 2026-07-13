#property strict
#include <AlphaLab/EXP0019/FaerieProtocol/I07/FP_I07_All.mqh>
input ENUM_TIMEFRAMES InpHostTimeframe=PERIOD_M5;
input bool InpRequireCompleteM1Coverage=true;
input bool InpPersistCheckpoint=true;
int OnInit()
{
   ENUM_TIMEFRAMES resolved; int seconds; string reason;
   if(!FP_I07_ResolveHostTimeframe(InpHostTimeframe,resolved,seconds,reason)) { Print("FP-I07 BLOCKED: ",reason); return INIT_FAILED; }
   Print("FP-I07 READY version=",FP_I07_ModuleVersion()," policy=",FP_I07_Policy()," tf=",EnumToString(resolved)," seconds=",seconds);
   return INIT_SUCCEEDED;
}
void OnTick() { }
