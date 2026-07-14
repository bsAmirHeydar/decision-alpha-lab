#ifndef __FP_I14_DIFFERENTIAL_COMPARATOR_MQH__
#define __FP_I14_DIFFERENTIAL_COMPARATOR_MQH__
#include "FP_I14_TraceLedger.mqh"
void FP_I14_CompareLedgers(const CFP_I14_TraceLedger &left,const CFP_I14_TraceLedger &right,FP_I14_DifferentialSummary &out){out.compared_events=MathMin(left.Count(),right.Count());out.mismatches=0;out.first_reason_code="";for(int i=0;i<out.compared_events;i++){FP_I14_TraceEvent a,b;left.Get(i,a);right.Get(i,b);if(FP_I14_EventFingerprint(a)!=FP_I14_EventFingerprint(b)){out.mismatches++;if(out.first_reason_code=="")out.first_reason_code="FP_DIAG_PAYLOAD_MISMATCH";}}if(left.Count()!=right.Count()){out.mismatches+=MathAbs(left.Count()-right.Count());if(out.first_reason_code=="")out.first_reason_code="FP_DIAG_EVENT_COUNT_MISMATCH";}out.status=(out.mismatches==0?FP_I14_STATUS_PASS:FP_I14_STATUS_FAIL);out.report_hash=FP_I14_HashText((string)out.compared_events+"|"+(string)out.mismatches+"|"+left.ChainHash()+"|"+right.ChainHash());}
#endif
