#property strict
#include <AlphaLab/EXP0019/FaerieProtocol/I07/FP_I07_All.mqh>
int OnInit()
{
   int failures=0;
   if(!FP_I07_ConfirmedEvidenceIsImmutable()) failures++;
   if(FP_I07_StateForOutcome(FP_I07_OUT_CONFIRMED)!=FP_I07_CONFIRMED) failures++;
   if(FP_I07_StateForOutcome(FP_I07_OUT_DEADLINE_MISSED)!=FP_I07_EXPIRED_DEADLINE) failures++;
   Print("FP-I07 self-test failures=",failures);
   return failures==0 ? INIT_SUCCEEDED : INIT_FAILED;
}
void OnTick() { }
