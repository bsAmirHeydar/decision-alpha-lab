#property strict
#property version "1.00"
#include <FaerieProtocol/EXP0019/Time/FP_I03_All.mqh>
int OnInit()
  {
   FP_I03_SelfTestResult result;bool ok=FP_I03_RunSelfTest(result);
   PrintFormat("FP-I03 self-test checks=%d pass=%d fail=%d evidence=%s latest=%s",result.check_count,result.pass_count,result.fail_count,result.evidence_key,result.latest_failed_check);
   return ok ? INIT_SUCCEEDED : INIT_FAILED;
  }
void OnTick(){}
