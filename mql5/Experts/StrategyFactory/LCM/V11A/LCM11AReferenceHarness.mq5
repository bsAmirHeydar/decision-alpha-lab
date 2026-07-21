#property strict
#include <StrategyFactory/LCM/V11A/LCM11ANamespace.mqh>
#include <StrategyFactory/LCM/V11A/LCM11AAnchorSemantics.mqh>
#include <StrategyFactory/LCM/V11A/LCM11ALifecycle.mqh>
int OnInit(){SLCM11A_VisualIdentity id;id.owner="REFERENCE";id.subsystem="LCM11A";id.instance_id="INSTANCE_1";id.chart_id=ChartID();id.symbol=_Symbol;id.timeframe=_Period;id.event_id="EVENT_1";id.role="REFERENCE";string name=LCM11A_ObjectId(id,"HARNESS");if(name=="")return INIT_FAILED;if(!LCM11A_CanTransition(LCM11A_VIS_UNINITIALIZED,LCM11A_VIS_INITIALIZED))return INIT_FAILED;Print("LCM-11A reference PASS ",name);return INIT_SUCCEEDED;}
void OnTick(){}
