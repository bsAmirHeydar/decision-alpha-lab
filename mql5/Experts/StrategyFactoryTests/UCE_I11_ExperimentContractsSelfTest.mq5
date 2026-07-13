#property strict
#property description "UCE-I11 registry, candidate, trial, and hidden-role contract self-test."

#include <AlphaLab/StrategyFactory/ExperimentOrchestration/UCEI11_All.mqh>

int OnInit()
  {
   int failures=0;
   CUCEI11SearchRegistry registry;
   if(!registry.BuildDefault()) failures++;
   registry.Freeze();
   if(!registry.Frozen() || registry.Count()!=10 || registry.NativeCount()!=9) failures++;

   UCEI11_SearchDescriptor descriptor;
   if(!registry.ResolveExact("uce.search.grid@1.0.0",descriptor) || !descriptor.Valid()) failures++;
   if(registry.ResolveExact("uce.search.grid@9.9.9",descriptor)) failures++;

   UCEI11_CandidateAdmission admitted;
   admitted.candidate_key="uce.classical.logistic";
   admitted.candidate_version="1.0.0";
   admitted.trainer_key="uce.classical.logistic_ridge@1.0.0";
   admitted.decision=UCEI11_ADMIT_ACCEPT;
   admitted.evidence_hash="hash";
   admitted.baseline=true;
   admitted.estimated_memory_mb=128;
   admitted.estimated_wall_seconds=5.0;
   admitted.requires_gpu=false;
   admitted.blockers="";
   if(!admitted.Valid() || !admitted.Schedulable()) failures++;

   UCEI11_CandidateAdmission rejected=admitted;
   rejected.decision=UCEI11_ADMIT_REJECT;
   rejected.blockers="future_perturbation_failed";
   if(!rejected.Valid() || rejected.Schedulable()) failures++;

   if(!CUCEI11DagValidation::HiddenRoleExcluded("final_test","train,validation")) failures++;
   if(CUCEI11DagValidation::HiddenRoleExcluded("final_test","train,final_test")) failures++;
   if(!CUCEI11DagValidation::BaselinePriorityBeforeChallenger(100,1000)) failures++;

   PrintFormat("UCE-I11 experiment-contract self-test failures=%d",failures);
   return failures==0 ? INIT_SUCCEEDED : INIT_FAILED;
  }

void OnTick() {}
