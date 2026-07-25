#property strict
#property description "UCE-I11 budget cutoff and reproducibility contract self-test."

#include <AlphaLab/StrategyFactory/ExperimentOrchestration/UCEI11_All.mqh>

int OnInit()
  {
   int failures=0;
   UCEI11_BudgetPolicy policy;
   policy.budget_id="b";
   policy.budget_version="1.0.0";
   policy.max_trials=2;
   policy.max_total_wall_seconds=100.0;
   policy.max_trial_wall_seconds=20.0;
   policy.max_memory_mb=1024;
   policy.cpu_slots=2;
   policy.gpu_slots=0;
   policy.max_retries=1;
   policy.max_artifact_bytes=1000000;
   policy.max_seeds=2;
   policy.max_folds=2;
   policy.max_candidates=2;
   policy.per_candidate_trial_cap=2;
   policy.retain_failed_artifacts=true;
   policy.fail_closed=true;

   CUCEI11BudgetGuard guard;
   if(!guard.Configure(policy)) failures++;

   UCEI11_ResourceClaim claim;
   claim.claim_id="c";
   claim.trial_id="t";
   claim.cpu_slots=1;
   claim.gpu_slots=0;
   claim.memory_mb=256;
   claim.wall_seconds=5.0;
   claim.artifact_bytes=100;
   claim.deterministic_required=true;
   string reason="";
   if(!guard.Reserve(claim,reason)) failures++;
   guard.Complete(2.0,50);
   UCEI11_BudgetUsage usage=guard.Usage();
   if(usage.trials_started!=1 || usage.trials_completed!=1) failures++;

   UCEI11_ResourceClaim too_large=claim;
   too_large.claim_id="c2";
   too_large.trial_id="t2";
   too_large.memory_mb=2048;
   if(guard.Assess(too_large,reason)!=UCEI11_BUDGET_DENY || reason!="memory_budget_exceeded") failures++;

   UCEI11_ReproducibilityReport report;
   report.report_id="r";
   report.manifest_hash="m";
   report.rerun_manifest_hash="m";
   report.declared_trial_count=2;
   report.executed_trial_count=2;
   report.selected_trial_hash_expected="s";
   report.selected_trial_hash_actual="s";
   report.event_stream_hash_expected="e";
   report.event_stream_hash_actual="e";
   report.passed=true;
   report.blockers="";
   report.warnings="";
   report.report_hash="h";
   if(!report.Valid() || !report.CountsReconcile()) failures++;

   PrintFormat("UCE-I11 budget/repro self-test failures=%d",failures);
   return failures==0 ? INIT_SUCCEEDED : INIT_FAILED;
  }

void OnTick() {}
