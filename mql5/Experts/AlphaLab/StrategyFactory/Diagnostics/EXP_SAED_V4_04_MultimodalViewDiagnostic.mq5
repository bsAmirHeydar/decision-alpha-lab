#property strict
#include <AlphaLab/StrategyFactory/SAEDV4MultimodalViews/ViewAll.mqh>
int OnInit(){ Print("SAED V4-04 views=",SAEDInstitutionalViewCount()," authority_safe=",SAEDViewAuthoritySafe()); return SAEDViewAuthoritySafe()?INIT_SUCCEEDED:INIT_FAILED; }
void OnTick(){}
