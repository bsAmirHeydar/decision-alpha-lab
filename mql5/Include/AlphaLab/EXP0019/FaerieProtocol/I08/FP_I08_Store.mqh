#ifndef FP_I08_STORE_MQH
#define FP_I08_STORE_MQH
#include "FP_I08_Contracts.mqh"
int FP_I08_FindContext(const FP_I08_WWContext &items[],const string id){for(int i=0;i<ArraySize(items);i++)if(items[i].context_id==id)return i;return -1;}
#endif
