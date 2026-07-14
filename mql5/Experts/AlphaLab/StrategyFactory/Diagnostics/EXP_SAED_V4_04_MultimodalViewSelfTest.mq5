#property strict
#include <AlphaLab/StrategyFactory/SAEDV4MultimodalViews/ViewAll.mqh>
int OnInit(){ if(SAEDInstitutionalViewCount()!=10)return INIT_FAILED; if(!SAEDViewMissingAllowed(SAED_MISSING_MASK))return INIT_FAILED; if(SAEDViewMissingAllowed(SAED_MISSING_PROHIBIT))return INIT_FAILED; return INIT_SUCCEEDED; }
void OnTick(){}
