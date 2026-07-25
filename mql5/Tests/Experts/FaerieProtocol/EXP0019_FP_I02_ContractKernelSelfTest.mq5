#property strict
#property version   "1.00"
#property description "EXP0019 FP-I02 contract, identity, reason-code, and lifecycle self-test"

#include <FaerieProtocol/EXP0019/Core/FP_I02_All.mqh>

int OnInit()
  {
   FP_I02_SelfTestResult result;
   bool passed=FP_I02_RunSelfTest(result);
   PrintFormat("FP-I02 self-test passed=%s checks=%d pass=%d fail=%d latest=%s evidence=%s",
               passed?"true":"false",result.check_count,result.pass_count,result.fail_count,
               result.latest_failed_check,result.evidence_key);
   return passed ? INIT_SUCCEEDED : INIT_FAILED;
  }

void OnTick() {}
