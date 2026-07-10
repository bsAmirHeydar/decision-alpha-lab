#ifndef __EXP0018_DAYE_VISUAL_SELF_TEST_MQH__
#define __EXP0018_DAYE_VISUAL_SELF_TEST_MQH__

#include <DayeTrader/EXP0018/DAYE_VisualObjectManager.mqh>

bool DAYE_RunEmbeddedVisualSelfTests(void)
{
   bool ok=true;
   ok=(DAYE_QuarterNumberFromCode("A")=="Q1")&&ok;
   ok=(DAYE_QuarterNumberFromCode("P")=="Q4")&&ok;
   ok=(DAYE_QuarterNumberFromCode("n3")=="Q3")&&ok;
   ok=(DAYE_ParentSessionCode("a4")=="A")&&ok;
   ok=(DAYE_PhaseLabel("p4")=="Q4 p4 30m")&&ok;
   string a=DAYE_VisualObjectName("TEST","same");
   string b=DAYE_VisualObjectName("TEST","same");
   ok=(a==b && DAYE_IsOwnedVisualObject(a))&&ok;
   if(!ok) Print("EXP0018 P10 embedded visual self-tests failed.");
   else Print("EXP0018 P10 embedded visual self-tests PASS.");
   return ok;
}

#endif
