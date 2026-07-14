#property strict
#include <AlphaLab/StrategyFactory/SAEDV4DataFoundation/DataFoundationAll.mqh>
int OnInit(){
 string reason="";
 ALBitemporalStamp stamp;stamp.event_time=D'2026.01.01 00:00:00';stamp.known_time=D'2026.01.01 00:00:01';stamp.valid_to=0;stamp.has_valid_to=false;
 if(!ALDataTemporalGate::Validate(stamp,reason)){Print("FAIL temporal ",reason);return(INIT_FAILED);}
 if(ALDataRoleGate::Allow(AL_ROLE_LIVE,AL_OP_TRAIN,reason)){Print("FAIL live training allowed");return(INIT_FAILED);}
 if(ALDataRoleGate::Allow(AL_ROLE_SYNTHETIC_STRESS,AL_OP_PROMOTE,reason)){Print("FAIL synthetic promotion allowed");return(INIT_FAILED);}
 Print("PASS SAED V4-01 self-test");return(INIT_SUCCEEDED);
}
void OnTick(){}
