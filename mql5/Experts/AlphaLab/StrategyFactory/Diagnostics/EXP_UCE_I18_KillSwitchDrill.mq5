#property strict
#include <AlphaLab/StrategyFactory/Qualification/QualificationKillSwitch.mqh>
int OnInit(){ ALKillSwitchState state; state.engaged=false; if(!ALEngageKillSwitch(state,"diagnostic",1000,StringRepeat("a",64))) return INIT_FAILED; if(!ALKillSwitchBlocksActions(state)) return INIT_FAILED; Print("UCE-I18 kill-switch drill passed"); return INIT_SUCCEEDED; }
void OnTick(){}
