#property strict
#include <StrategyFactory/LCM/V10B/LCM10BStaticContract.mqh>
#include <StrategyFactory/LCM/V10B/LCM10BDisabledAdapter.mqh>
int OnInit(){ CLCM10BDisabledAdapter adapter; if(adapter.SubmissionEnabled()) return INIT_FAILED; Print("LCM-10B reference boundary loaded; broker mutation unavailable."); return INIT_SUCCEEDED; }
void OnTick(){ }
