#property strict
#property version "1.00"
#include <FaerieProtocol/EXP0019/Data/FP_I04_All.mqh>
int OnInit(){FP_I04_SelfTestResult result;bool ok=FP_I04_RunSelfTest(result);PrintFormat("FP-I04 self-test checks=%d pass=%d fail=%d evidence=%s latest=%s",result.check_count,result.pass_count,result.fail_count,result.evidence_key,result.latest_failed_check);return ok?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
