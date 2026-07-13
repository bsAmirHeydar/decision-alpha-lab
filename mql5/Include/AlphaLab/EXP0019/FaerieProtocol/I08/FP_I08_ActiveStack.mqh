#ifndef FP_I08_STACK_MQH
#define FP_I08_STACK_MQH
#include "FP_I08_Contracts.mqh"
bool FP_I08_ResolveActiveStack(const FP_I08_WWContext &items[],const datetime at,FP_I08_ActiveStack &out){int winner=-1;datetime latest=0;for(int i=0;i<ArraySize(items);i++){if(items[i].state==FP_I08_WW_CONFIRMED&&items[i].confirmed_time<=at&&at<items[i].week_end&&(winner<0||items[i].confirmed_time>latest)){winner=i;latest=items[i].confirmed_time;}}if(winner<0){out.active_context_id="";out.active_signal_id="";out.active_direction=-1;out.reason_code="FP_RC_WW_NONE_ALLOW_BOTH";return true;}out.active_context_id=items[winner].context_id;out.active_signal_id=items[winner].signal_id;out.active_direction=items[winner].direction;out.reason_code="FP_WRC_NEWEST_ACTIVE_WW_WINS";return true;}
#endif
