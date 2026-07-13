#ifndef __UCEI11_CONTRACTS_MQH__
#define __UCEI11_CONTRACTS_MQH__

#include "UCEI11_Enums.mqh"

struct UCEI11_CandidateAdmission
  {
   string                     candidate_key;
   string                     candidate_version;
   string                     trainer_key;
   UCEI11_ADMISSION_DECISION  decision;
   string                     evidence_hash;
   bool                       baseline;
   int                        estimated_memory_mb;
   double                     estimated_wall_seconds;
   bool                       requires_gpu;
   string                     blockers;

   bool Schedulable() const
     {
      return decision==UCEI11_ADMIT_ACCEPT || decision==UCEI11_ADMIT_WARN;
     }

   bool Valid() const
     {
      if(candidate_key=="" || candidate_version=="" || trainer_key=="" || evidence_hash=="")
         return false;
      if(estimated_memory_mb<1 || estimated_wall_seconds<=0.0)
         return false;
      if(decision==UCEI11_ADMIT_REJECT && blockers=="")
         return false;
      if(decision!=UCEI11_ADMIT_REJECT && blockers!="")
         return false;
      return true;
     }
  };

struct UCEI11_BudgetPolicy
  {
   string budget_id;
   string budget_version;
   int    max_trials;
   double max_total_wall_seconds;
   double max_trial_wall_seconds;
   int    max_memory_mb;
   int    cpu_slots;
   int    gpu_slots;
   int    max_retries;
   long   max_artifact_bytes;
   int    max_seeds;
   int    max_folds;
   int    max_candidates;
   int    per_candidate_trial_cap;
   bool   retain_failed_artifacts;
   bool   fail_closed;

   bool Valid() const
     {
      if(budget_id=="" || budget_version=="")
         return false;
      if(max_trials<1 || max_total_wall_seconds<=0.0 || max_trial_wall_seconds<=0.0)
         return false;
      if(max_trial_wall_seconds>max_total_wall_seconds)
         return false;
      if(max_memory_mb<1 || cpu_slots<1 || gpu_slots<0 || max_retries<0)
         return false;
      if(max_artifact_bytes<1 || max_seeds<1 || max_folds<1 || max_candidates<1)
         return false;
      if(per_candidate_trial_cap<1 || per_candidate_trial_cap>max_trials)
         return false;
      return true;
     }
  };

struct UCEI11_ResourceClaim
  {
   string claim_id;
   string trial_id;
   int    cpu_slots;
   int    gpu_slots;
   int    memory_mb;
   double wall_seconds;
   long   artifact_bytes;
   bool   deterministic_required;

   bool Valid() const
     {
      return claim_id!="" && trial_id!="" && cpu_slots>=1 && gpu_slots>=0 &&
             memory_mb>=1 && wall_seconds>0.0 && artifact_bytes>=0;
     }
  };

struct UCEI11_TrialIdentity
  {
   string trial_id;
   string experiment_id;
   string candidate_key;
   string trainer_key;
   string parameter_hash;
   string fold_id;
   int    seed;
   int    resource_level;
   string dataset_manifest_hash;
   string split_plan_hash;
   string transform_plan_hash;
   string target_plan_hash;
   string economics_plan_hash;
   string known_time_policy_hash;
   string search_plan_hash;
   string budget_policy_hash;
   string scheduler_version;
   string compiler_version;
   string identity_hash;

   bool Valid() const
     {
      if(trial_id=="" || experiment_id=="" || candidate_key=="" || trainer_key=="")
         return false;
      if(parameter_hash=="" || fold_id=="" || seed<0 || resource_level<1)
         return false;
      if(dataset_manifest_hash=="" || split_plan_hash=="" || transform_plan_hash=="")
         return false;
      if(target_plan_hash=="" || economics_plan_hash=="" || known_time_policy_hash=="")
         return false;
      if(search_plan_hash=="" || budget_policy_hash=="" || identity_hash=="")
         return false;
      return scheduler_version!="" && compiler_version!="";
     }
  };

struct UCEI11_DagNode
  {
   string           node_id;
   UCEI11_NODE_KIND kind;
   string           semantic_key;
   string           payload_hash;
   string           dependency_ids;
   int              priority;
   string           resource_claim_hash;
   string           trial_id;

   bool Valid() const
     {
      return node_id!="" && semantic_key!="" && payload_hash!="" && priority>=0;
     }
  };

struct UCEI11_SchedulerEvent
  {
   string             event_id;
   int                sequence;
   string             node_id;
   string             trial_id;
   string             event_kind;
   UCEI11_NODE_STATUS status_before;
   UCEI11_NODE_STATUS status_after;
   int                attempt;
   string             worker_id;
   string             payload_hash;
   string             reason_code;

   bool Valid() const
     {
      return event_id!="" && sequence>=0 && node_id!="" && event_kind!="" &&
             attempt>=0 && payload_hash!="";
     }
  };

struct UCEI11_SelectionLedgerEntry
  {
   string entry_id;
   int    sequence;
   string experiment_id;
   string manifest_hash;
   string trial_id;
   string node_id;
   string action;
   string reason_code;
   string artifact_hashes;
   string actor;
   string previous_entry_hash;
   string entry_hash;

   bool Valid() const
     {
      return entry_id!="" && sequence>=0 && experiment_id!="" && manifest_hash!="" &&
             trial_id!="" && node_id!="" && action!="" && actor!="" && entry_hash!="";
     }
  };

struct UCEI11_CacheRecord
  {
   string cache_key;
   string namespace_name;
   string artifact_kind;
   string producer_version;
   string schema_version;
   string input_hashes;
   string payload_hash;
   string provenance_hash;
   int    created_sequence;
   long   size_bytes;

   bool Valid() const
     {
      return cache_key!="" && namespace_name!="" && artifact_kind!="" &&
             producer_version!="" && schema_version!="" && input_hashes!="" &&
             payload_hash!="" && provenance_hash!="" && created_sequence>=0 && size_bytes>=0;
     }
  };

struct UCEI11_ReproducibilityReport
  {
   string report_id;
   string manifest_hash;
   string rerun_manifest_hash;
   int    declared_trial_count;
   int    executed_trial_count;
   string selected_trial_hash_expected;
   string selected_trial_hash_actual;
   string event_stream_hash_expected;
   string event_stream_hash_actual;
   bool   passed;
   string blockers;
   string warnings;
   string report_hash;

   bool CountsReconcile() const
     {
      return declared_trial_count==executed_trial_count;
     }

   bool Valid() const
     {
      if(report_id=="" || manifest_hash=="" || rerun_manifest_hash=="" || report_hash=="")
         return false;
      if(declared_trial_count<0 || executed_trial_count<0)
         return false;
      if(passed && blockers!="")
         return false;
      if(!passed && blockers=="")
         return false;
      return true;
     }
  };

#endif
