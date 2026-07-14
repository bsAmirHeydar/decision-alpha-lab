#property strict
#include <AlphaLab/EXP0019/FaerieProtocol/I09/FP_I09_All.mqh>
int OnInit(){ Print("FP-I09 ledger diagnostic version=",FP_I09_PHASE_VERSION," quota=",FP_I09_QUOTA_SCOPE," consumption=",FP_I09_CONSUMPTION_POLICY); return INIT_SUCCEEDED; }
void OnTick(){}
