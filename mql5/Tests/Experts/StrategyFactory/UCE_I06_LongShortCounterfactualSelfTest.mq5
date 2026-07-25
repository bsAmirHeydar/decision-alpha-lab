#property strict
#include <AlphaLab/StrategyFactory/OutcomeDataset/UCEI06_All.mqh>
int OnInit(){
 UCEI06_PathObservation p[3];for(int i=0;i<3;i++){p[i].sequence=i;p[i].event_time_ms=1000+i*1000;p[i].known_time_ms=p[i].event_time_ms;p[i].bid=1.1000+i*0.0006;p[i].ask=p[i].bid+0.0001;p[i].available_volume=2.0;p[i].gap=false;}
 if(!(p[0].ask>p[0].bid))return INIT_FAILED;Print("UCE-I06 long/short executable-side fixture PASS");return INIT_SUCCEEDED;}
void OnTick(){}
