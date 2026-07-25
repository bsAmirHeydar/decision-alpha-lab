#property strict
#include <AlphaLab/EXP0019/FaerieProtocol/I09/FP_I09_All.mqh>
int OnInit(){ FP_I09_Contender x[]; ArrayResize(x,2); x[0].signal_id="B";x[0].first_hunt_m1=120;x[0].confirmation_close=300;x[0].relation="AL";x[0].direction="BULLISH";x[0].hunter_symbol="ES"; x[1]=x[0];x[1].signal_id="A";x[1].first_hunt_m1=60; if(FP_I09_FindWinner(x)!=1) return INIT_FAILED; if(FP_I09_LiveConsumptionAllowed()) return INIT_FAILED; Print("FP-I09 SELFTEST PASS"); return INIT_SUCCEEDED; }
void OnTick(){}
