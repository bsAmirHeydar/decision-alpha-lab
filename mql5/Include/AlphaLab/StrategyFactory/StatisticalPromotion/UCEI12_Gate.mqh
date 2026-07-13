#ifndef __UCEI12_GATE_MQH__
#define __UCEI12_GATE_MQH__

#include "UCEI12_Scorecard.mqh"

class CUCEI12PromotionGate
  {
public:
   static UCEI12_GATE_OUTCOME Decide(const UCEI12_PromotionPolicy &policy,
                                     const CUCEI12Scorecard &scorecard,
                                     const UCEI12_SelectionUniverse &universe,
                                     const UCEI12_UncertaintyReport &uncertainty,
                                     const UCEI12_MultiplicityReport &multiplicity,
                                     const double pbo,
                                     const double deflated_probability,
                                     const double reality_check_p,
                                     const double minimum_stress_retention,
                                     const double ece,
                                     const bool mandatory_nulls_passed,
                                     const bool prospective_frozen,
                                     const bool signed_bundle,
                                     const bool manual_override_present,
                                     string &reason)
     {
      reason="";
      if(!policy.Valid() || !universe.Valid() || !uncertainty.Valid() || !multiplicity.Valid())
        {
         reason="invalid_contract";
         return UCEI12_GATE_REJECT;
        }
      if(scorecard.CriticalBlockers()>0)
        {
         reason="critical_blocker";
         return UCEI12_GATE_REJECT;
        }
      if(uncertainty.effective_sample_size<policy.minimum_effective_sample_size)
        {
         reason="insufficient_effective_sample_size";
         return UCEI12_GATE_REJECT;
        }
      if(multiplicity.total_choice_count!=universe.declared_trial_count)
        {
         reason="multiplicity_universe_mismatch";
         return UCEI12_GATE_REJECT;
        }
      if(pbo>policy.maximum_pbo || deflated_probability<policy.minimum_deflated_probability || reality_check_p>policy.maximum_reality_check_p)
        {
         reason="winner_overfit_gate_failed";
         return UCEI12_GATE_REJECT;
        }
      if(!mandatory_nulls_passed || minimum_stress_retention<policy.minimum_stress_retention)
        {
         reason="null_or_stress_gate_failed";
         return UCEI12_GATE_REJECT;
        }
      if(!prospective_frozen || (policy.require_signed_bundle && !signed_bundle))
        {
         reason="prospective_or_signature_gate_failed";
         return UCEI12_GATE_REJECT;
        }
      if(manual_override_present && !policy.allow_manual_override_to_promote)
        {
         reason="manual_override_present";
         return UCEI12_GATE_REJECT;
        }
      if(scorecard.Score()<policy.minimum_score || ece>policy.maximum_ece || scorecard.HighRisks()>0)
        {
         reason="challenge_required";
         return UCEI12_GATE_CHALLENGE;
        }
      return UCEI12_GATE_PROMOTE;
     }
  };

#endif
