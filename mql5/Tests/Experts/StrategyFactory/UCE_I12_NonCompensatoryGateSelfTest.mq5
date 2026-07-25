#property strict
#property version "1.00"
#property description "UCE-I12 critical blocker non-compensation self-test"

#include "../../Include/AlphaLab/StrategyFactory/StatisticalPromotion/UCEI12_All.mqh"

int OnInit()
  {
   CUCEI12Scorecard scorecard; scorecard.Reset();
   UCEI12_TestEvidence evidence;
   evidence.test_id="known_time"; evidence.family="integrity"; evidence.status=UCEI12_EVIDENCE_FAIL;
   evidence.severity=UCEI12_SEVERITY_CRITICAL; evidence.blocker_code="known_time_leakage"; evidence.evidence_hash="hash";
   if(!scorecard.Add(evidence,1.0)) return INIT_FAILED;
   if(scorecard.CriticalBlockers()!=1 || scorecard.Score()!=0.0) return INIT_FAILED;
   Print("UCE-I12 non-compensatory gate self-test PASS");
   return INIT_SUCCEEDED;
  }

void OnTick() {}
