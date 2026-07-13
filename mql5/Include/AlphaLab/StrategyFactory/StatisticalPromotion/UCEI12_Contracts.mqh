#ifndef __UCEI12_CONTRACTS_MQH__
#define __UCEI12_CONTRACTS_MQH__

#include "UCEI12_Enums.mqh"

struct UCEI12_TrialEvidence
  {
   string                    trial_id;
   string                    family_id;
   string                    candidate_key;
   UCEI12_TRIAL_DISPOSITION  disposition;
   string                    ledger_entry_hash;
   double                    p_value;
   bool                      has_p_value;
   bool                      integrity_blocked;

   bool Valid() const
     {
      if(trial_id=="" || family_id=="" || candidate_key=="" || ledger_entry_hash=="")
         return false;
      if(has_p_value && (p_value<0.0 || p_value>1.0))
         return false;
      return true;
     }
  };

struct UCEI12_SelectionUniverse
  {
   string universe_id;
   string manifest_hash;
   string ledger_hash;
   int    declared_trial_count;
   int    observed_trial_count;
   bool   ledger_complete;

   bool Valid() const
     {
      return universe_id!="" && manifest_hash!="" && ledger_hash!="" &&
             declared_trial_count>0 && declared_trial_count==observed_trial_count && ledger_complete;
     }
  };

struct UCEI12_UncertaintyReport
  {
   double estimate;
   double lower;
   double upper;
   double effective_sample_size;
   string evidence_hash;

   bool Valid() const
     {
      return lower<=upper && effective_sample_size>0.0 && evidence_hash!="";
     }
  };

struct UCEI12_MultiplicityReport
  {
   int    total_choice_count;
   int    tested_choice_count;
   int    missing_p_value_count;
   string universe_hash;
   string evidence_hash;

   bool Valid() const
     {
      return total_choice_count>0 && tested_choice_count>=0 && missing_p_value_count>=0 &&
             tested_choice_count+missing_p_value_count==total_choice_count &&
             universe_hash!="" && evidence_hash!="";
     }
  };

struct UCEI12_TestEvidence
  {
   string                  test_id;
   string                  family;
   UCEI12_EVIDENCE_STATUS  status;
   UCEI12_SEVERITY         severity;
   string                  blocker_code;
   string                  evidence_hash;

   bool Valid() const
     {
      if(test_id=="" || family=="" || evidence_hash=="")
         return false;
      if(status==UCEI12_EVIDENCE_FAIL && blocker_code=="")
         return false;
      if(status==UCEI12_EVIDENCE_PASS && blocker_code!="")
         return false;
      return true;
     }
  };

struct UCEI12_PromotionPolicy
  {
   string policy_id;
   string policy_version;
   double minimum_score;
   double minimum_effective_sample_size;
   double maximum_pbo;
   double minimum_deflated_probability;
   double maximum_reality_check_p;
   double minimum_stress_retention;
   double maximum_ece;
   bool   require_signed_bundle;
   bool   allow_manual_override_to_promote;

   bool Valid() const
     {
      return policy_id!="" && policy_version!="" &&
             minimum_score>=0.0 && minimum_score<=1.0 &&
             minimum_effective_sample_size>0.0 &&
             maximum_pbo>=0.0 && maximum_pbo<=1.0 &&
             minimum_deflated_probability>=0.0 && minimum_deflated_probability<=1.0 &&
             maximum_reality_check_p>=0.0 && maximum_reality_check_p<=1.0 &&
             minimum_stress_retention>=0.0 && minimum_stress_retention<=1.0 &&
             maximum_ece>=0.0 && maximum_ece<=1.0;
     }
  };

struct UCEI12_PromotionDecision
  {
   string               decision_id;
   string               candidate_key;
   UCEI12_GATE_OUTCOME  outcome;
   string               blockers_csv;
   string               challenges_csv;
   string               evidence_bundle_hash;
   bool                 signed_bundle;

   bool Valid() const
     {
      if(decision_id=="" || candidate_key=="" || evidence_bundle_hash=="")
         return false;
      if(outcome==UCEI12_GATE_PROMOTE && (blockers_csv!="" || !signed_bundle))
         return false;
      if(outcome==UCEI12_GATE_REJECT && blockers_csv=="")
         return false;
      return true;
     }
  };

#endif
