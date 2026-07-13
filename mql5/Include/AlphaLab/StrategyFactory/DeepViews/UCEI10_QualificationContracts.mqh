#ifndef __UCEI10_QUALIFICATION_CONTRACTS_MQH__
#define __UCEI10_QUALIFICATION_CONTRACTS_MQH__

#include "UCEI10_Enums.mqh"

struct UCEI10_DeepAdmissionEvidence
  {
   string                    evidence_id;
   string                    dataset_id;
   string                    dataset_manifest_hash;
   double                    effective_sample_size;
   int                       dependence_cluster_count;
   int                       event_diversity_count;
   bool                      stable_dimensions;
   bool                      known_time_audit_passed;
   bool                      future_perturbation_passed;
   bool                      classical_gate_passed;
   double                    classical_best_metric;
   string                    augmentation_policy_hash;
   string                    ablation_plan_hash;
   UCEI10_ADMISSION_DECISION decision;
   string                    blockers;
   string                    warnings;
   string                    evidence_hash;

   bool AcceptedForResearch() const
     {
      return decision!=UCEI10_ADMIT_REJECT &&
             stable_dimensions && known_time_audit_passed &&
             future_perturbation_passed && classical_gate_passed;
     }

   bool AcceptedForPromotion() const
     {
      return decision==UCEI10_ADMIT_ACCEPT && AcceptedForResearch();
     }
  };

struct UCEI10_SeedRunObservation
  {
   int    seed;
   string status;
   double primary_metric;
   double economic_utility;
   double calibration_error;
   long   fit_ms;
   long   predict_ms;
   string artifact_hash;
   string error_code;

   bool Succeeded() const
     {
      return status=="succeeded" && artifact_hash!="" &&
             MathIsValidNumber(primary_metric) &&
             MathIsValidNumber(economic_utility) &&
             MathIsValidNumber(calibration_error) &&
             fit_ms>=0 && predict_ms>=0;
     }
  };

struct UCEI10_ExportAssessment
  {
   UCEI10_EXPORT_PATH path;
   bool               available;
   double             parity_max_abs_error;
   double             latency_ms;
   string             artifact_hash;
   string             reason;
   string             evidence_hash;

   bool Valid() const
     {
      if(!MathIsValidNumber(parity_max_abs_error) || parity_max_abs_error<0.0)
         return false;
      if(!MathIsValidNumber(latency_ms) || latency_ms<0.0)
         return false;
      if(available && path==UCEI10_EXPORT_NONE)
         return false;
      return evidence_hash!="";
     }
  };

struct UCEI10_DeepQualificationReport
  {
   string                       report_id;
   string                       algorithm_key;
   string                       dataset_manifest_hash;
   string                       admission_evidence_id;
   int                          seed_run_count;
   int                          successful_seed_count;
   int                          ablation_count;
   double                       baseline_metric;
   double                       mean_metric;
   double                       metric_std;
   double                       mean_economic_utility;
   double                       failed_run_rate;
   double                       minimum_incremental_uplift;
   UCEI10_QUALIFICATION_DECISION decision;
   string                       blockers;
   string                       warnings;
   string                       evidence_hash;

   bool Promotable() const
     {
      return decision==UCEI10_PROMOTABLE && seed_run_count>=3 &&
             successful_seed_count>=3 && ablation_count>0 &&
             failed_run_rate>=0.0 && failed_run_rate<=0.2 &&
             mean_economic_utility>0.0 && evidence_hash!="";
     }
  };

#endif
