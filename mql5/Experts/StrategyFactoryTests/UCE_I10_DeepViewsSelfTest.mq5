#property strict
#property description "UCE-I10 catalog, admission, and view-contract self-test."

#include <AlphaLab/StrategyFactory/DeepViews/UCEI10_All.mqh>

int OnInit()
  {
   int failures=0;

   CUCEI10Registry registry;
   if(!registry.BuildDefault())
      failures++;
   registry.Freeze();
   if(!registry.Frozen() || registry.Count()!=17 || registry.NativeCount()!=10)
      failures++;

   UCEI10_AlgorithmDescriptor descriptor;
   if(!registry.ResolveExact("causal_temporal_conv_ridge@1.0.0",descriptor) || !descriptor.Valid())
      failures++;
   if(registry.ResolveExact("causal_temporal_conv_ridge@9.9.9",descriptor))
      failures++;

   UCEI10_ViewTensorSpec view;
   view.view_id="sequence";
   view.view_version="1.0.0";
   view.view_kind="sequence";
   view.layout="time_major";
   view.feature_order="close,range,age";
   view.context_observation_id="ctx";
   view.known_time_ms=100;
   view.mask_required=true;
   view.runtime_exportable=true;
   ArrayResize(view.shape,2);
   view.shape[0]=8;
   view.shape[1]=3;
   if(!view.Valid() || view.Width()!=24)
      failures++;

   UCEI10_SequenceArtifact sequence;
   sequence.artifact_id="seq";
   sequence.spec_hash="spec";
   sequence.context_observation_id="ctx";
   sequence.known_time_ms=100;
   sequence.step_count=8;
   sequence.channel_count=3;
   sequence.value_count=24;
   sequence.mask_count=24;
   sequence.source_hash="source";
   sequence.evidence_hash="evidence";
   if(!sequence.Valid())
      failures++;

   UCEI10_DeepAdmissionEvidence admission;
   admission.evidence_id="e";
   admission.dataset_id="d";
   admission.dataset_manifest_hash="m";
   admission.effective_sample_size=1000.0;
   admission.dependence_cluster_count=100;
   admission.event_diversity_count=4;
   admission.stable_dimensions=true;
   admission.known_time_audit_passed=true;
   admission.future_perturbation_passed=true;
   admission.classical_gate_passed=true;
   admission.classical_best_metric=0.61;
   admission.augmentation_policy_hash="a";
   admission.ablation_plan_hash="b";
   admission.decision=UCEI10_ADMIT_ACCEPT;
   admission.evidence_hash="h";
   if(!admission.AcceptedForResearch() || !admission.AcceptedForPromotion())
      failures++;

   PrintFormat("UCE-I10 self-test failures=%d",failures);
   return failures==0 ? INIT_SUCCEEDED : INIT_FAILED;
  }

void OnTick()
  {
  }
