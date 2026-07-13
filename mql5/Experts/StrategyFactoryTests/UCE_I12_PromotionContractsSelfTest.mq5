#property strict
#property version "1.00"
#property description "UCE-I12 promotion contract self-test"

#include "../../Include/AlphaLab/StrategyFactory/StatisticalPromotion/UCEI12_All.mqh"

int OnInit()
  {
   UCEI12_SelectionUniverse universe;
   universe.universe_id="golden"; universe.manifest_hash="manifest"; universe.ledger_hash="ledger";
   universe.declared_trial_count=9; universe.observed_trial_count=9; universe.ledger_complete=true;
   UCEI12_MultiplicityReport multiplicity;
   multiplicity.total_choice_count=9; multiplicity.tested_choice_count=3; multiplicity.missing_p_value_count=6;
   multiplicity.universe_hash="universe"; multiplicity.evidence_hash="evidence";
   if(!universe.Valid() || !multiplicity.Valid()) return INIT_FAILED;
   Print("UCE-I12 contract self-test PASS");
   return INIT_SUCCEEDED;
  }

void OnTick() {}
