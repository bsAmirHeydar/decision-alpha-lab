#ifndef __FP_I09_QUOTA_ARBITER_MQH__
#define __FP_I09_QUOTA_ARBITER_MQH__
#include "FP_I09_Ranking.mqh"
int FP_I09_FindWinner(FP_I09_Contender &items[]){ if(ArraySize(items)==0) return -1; int w=0; for(int i=1;i<ArraySize(items);i++) if(FP_I09_Compare(items[i],items[w])<0) w=i; return w; }
bool FP_I09_LiveConsumptionAllowed(){ return false; } // FP-DEC-012 remains UNSET
#endif
