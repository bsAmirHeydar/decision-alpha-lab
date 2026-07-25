#property strict
#property description "UCE-I10 negative contract and fail-closed safety self-test."

#include <AlphaLab/StrategyFactory/DeepViews/UCEI10_All.mqh>

int OnInit()
  {
   int failures=0;

   UCEI10_ViewTensorSpec view;
   view.view_id="graph";
   view.view_version="1.0.0";
   view.view_kind="graph";
   view.layout="node_major";
   view.context_observation_id="ctx";
   view.known_time_ms=-1;
   ArrayResize(view.shape,2);
   view.shape[0]=4;
   view.shape[1]=3;
   if(view.Valid())
      failures++;
   view.known_time_ms=100;
   if(!view.Valid())
      failures++;

   UCEI10_RegimeNoveltyPrediction regime;
   regime.prediction_id="p";
   regime.row_id="r";
   regime.regime_id="regime_0";
   regime.regime_probability=1.2;
   regime.novelty_score=0.1;
   regime.change_score=0.0;
   regime.support_count=1;
   regime.reason="invalid_probability";
   regime.evidence_hash="h";
   if(regime.Valid())
      failures++;
   regime.regime_probability=0.8;
   regime.decision=UCEI10_ABSTAIN;
   if(!regime.Valid())
      failures++;

   UCEI10_FusionPrediction fusion;
   fusion.prediction_id="f";
   fusion.row_id="r";
   fusion.fusion_kind=UCEI10_FUSION_LATE_WEIGHTED;
   fusion.missing_policy=UCEI10_MISSING_ABSTAIN;
   fusion.available_view_count=2;
   fusion.missing_view_count=0;
   fusion.weight_sum=0.5;
   fusion.value=1.0;
   fusion.uncertainty=0.1;
   fusion.abstained=false;
   fusion.reason="fused";
   fusion.evidence_hash="h";
   if(fusion.Valid())
      failures++;
   fusion.weight_sum=1.0;
   if(!fusion.Valid())
      failures++;

   UCEI10_TransferBoundary transfer;
   transfer.boundary_id="t";
   transfer.source_dataset_manifest_hash="s";
   transfer.target_dataset_manifest_hash="d";
   transfer.source_row_ids_hash="sr";
   transfer.target_train_row_ids_hash="tr";
   transfer.target_final_test_row_ids_hash="te";
   transfer.representation_frozen=true;
   transfer.decision=UCEI10_TRANSFER_REJECT;
   transfer.blockers="source_contains_target_final_test_rows";
   transfer.evidence_hash="h";
   if(transfer.Accepted())
      failures++;

   PrintFormat("UCE-I10 causality/safety failures=%d",failures);
   return failures==0 ? INIT_SUCCEEDED : INIT_FAILED;
  }

void OnTick()
  {
  }
