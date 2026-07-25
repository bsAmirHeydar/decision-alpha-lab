#property strict
#property version   "1.00"
#property description "EXP0019 FP-I01 shared-core adapter compatibility self-test"

#include <FaerieProtocol/EXP0019/Compatibility/FP_I01_All.mqh>

int OnInit()
  {
   FP_I01_SelfTestResult result;
   bool ok=FP_I01_RunSelfTest(result);
   PrintFormat("FP-I01 self-test: ok=%s checks=%d pass=%d fail=%d latest=%s evidence=%s",
               ok ? "true" : "false",result.check_count,result.pass_count,result.fail_count,
               result.latest_failed_check,result.evidence_key);
   return ok ? INIT_SUCCEEDED : INIT_FAILED;
  }

void OnTick() {}
