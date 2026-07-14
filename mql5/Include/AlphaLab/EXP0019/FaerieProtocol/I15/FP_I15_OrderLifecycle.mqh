#ifndef FP_I15_ORDER_LIFECYCLE_MQH
#define FP_I15_ORDER_LIFECYCLE_MQH
#include "FP_I15_Contracts.mqh"
#include "FP_I15_Hash.mqh"
bool FP_I15_OrderTransition(FP_I15_PaperOrder &o,const FP_I15_ORDER_STATE next){ bool ok=false; if(o.state==FP_I15_ORDER_CREATED)ok=(next==FP_I15_ORDER_VALIDATED||next==FP_I15_ORDER_REJECTED); else if(o.state==FP_I15_ORDER_VALIDATED)ok=(next==FP_I15_ORDER_ATTEMPTED||next==FP_I15_ORDER_REJECTED); else if(o.state==FP_I15_ORDER_ATTEMPTED)ok=(next==FP_I15_ORDER_ACCEPTED||next==FP_I15_ORDER_REJECTED); else if(o.state==FP_I15_ORDER_ACCEPTED)ok=(next==FP_I15_ORDER_PARTIAL||next==FP_I15_ORDER_FILLED||next==FP_I15_ORDER_CANCELLED); else if(o.state==FP_I15_ORDER_PARTIAL)ok=(next==FP_I15_ORDER_PARTIAL||next==FP_I15_ORDER_FILLED||next==FP_I15_ORDER_CANCELLED); if(ok)o.state=next; return ok; }
#endif
