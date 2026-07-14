#property strict
#property description "FP-I14 non-trading diagnostic self-test"
#include <AlphaLab/EXP0019/FaerieProtocol/I14/FP_I14_All.mqh>
int OnInit(){
 CFP_I14_TraceLedger left,right;string reason;
 for(int i=1;i<=16;i++){FP_I14_TraceEvent a;a.sequence=i;a.event_time=TimeCurrent()+i;a.product=FP_I14_PRODUCT_INDICATOR;a.event_type=(ENUM_FP_I14_EVENT)(i-1);a.semantic_id="SEM-"+(string)i;a.payload_hash=FP_I14_HashText(a.semantic_id);a.config_hash="CONFIG";a.source_revision_id="REV-1";a.state="READY";a.buffer_index=(i==14?0:-1);a.numeric_value=i;FP_I14_TraceEvent b=a;b.product=FP_I14_PRODUCT_DIAGNOSTIC_EA;if(!left.Append(a,reason)||!right.Append(b,reason)){Print("FAIL ",reason);return INIT_FAILED;}}
 FP_I14_DifferentialSummary d;FP_I14_CompareLedgers(left,right,d);if(d.status!=FP_I14_STATUS_PASS||d.mismatches!=0){Print("FAIL differential");return INIT_FAILED;}
 bool ok=FP_I14_SourceAcceptance(d.mismatches,true,true,reason);if(!ok){Print("FAIL gate ",reason);return INIT_FAILED;}
 Print("FP-I14 SELF TEST PASS; authority NONE; events=",d.compared_events);return INIT_SUCCEEDED;
}
void OnTick(){}
