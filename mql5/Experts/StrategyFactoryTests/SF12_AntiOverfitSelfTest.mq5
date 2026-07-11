#property strict
#include <AlphaLab/StrategyFactory/Validation/SF12_AllValidation.mqh>
int OnInit()
{
   SF12_ValidationPlan p;p.schema="alpha_lab.strategy_factory/validation_plan@1.0.0";p.plan_id="sf12_selftest";p.plan_version="1.0.0";p.method=SF12_SPLIT_ANCHORED_WALK_FORWARD;
   p.source_run_id="run_selftest";p.source_manifest_hash="manifest_hash";p.source_artifact_hash="artifact_hash";p.strategy_id="reference_strategy";p.search_space_hash="search_hash";
   p.start_utc_msc=0;p.end_utc_msc=200000;p.train_span_msc=40000;p.validation_span_msc=10000;p.test_span_msc=10000;p.step_span_msc=20000;p.purge_span_msc=1000;p.embargo_span_msc=1000;
   p.minimum_train_samples=1;p.minimum_validation_samples=1;p.minimum_test_samples=1;p.maximum_folds=8;p.random_seed=12;p.plan_hash=SF12_DeriveValidationPlanHash(p);
   string error;SF12_ValidationFold folds[];CSF12FoldCompiler compiler;if(!compiler.Compile(p,folds,error)||ArraySize(folds)<4){Print("SF12 fold compiler failed: ",error);return INIT_FAILED;}
   CSF12ValidationEngine engine;
   for(int i=0;i<ArraySize(folds);i++)
   {
      SF12_FoldObservation tr;tr.schema="alpha_lab.strategy_factory/fold_observation@1.0.0";tr.observation_id="train_"+IntegerToString(i);tr.trial_id="trial_a";tr.parameter_hash="parameter_hash";tr.fold_id=folds[i].fold_id;tr.role=SF12_ROLE_TRAIN;tr.event_id="event_train_"+IntegerToString(i);tr.cluster_id="cluster_train_"+IntegerToString(i);tr.outcome_id="outcome_train_"+IntegerToString(i);tr.known_time_utc_msc=folds[i].train.start_utc_msc+1;tr.resolved_time_utc_msc=tr.known_time_utc_msc+1;tr.net_r=0.20;tr.gross_r=0.22;tr.cost_r=0.02;tr.ambiguous=false;tr.observation_hash=SF12_DeriveFoldObservationHash(tr);if(!engine.Observe(tr,error)){Print(error);return INIT_FAILED;}
      SF12_FoldObservation te=tr;te.observation_id="test_"+IntegerToString(i);te.role=SF12_ROLE_TEST;te.event_id="event_test_"+IntegerToString(i);te.cluster_id="cluster_test_"+IntegerToString(i);te.outcome_id="outcome_test_"+IntegerToString(i);te.known_time_utc_msc=folds[i].test.start_utc_msc+1;te.resolved_time_utc_msc=te.known_time_utc_msc+1;te.net_r=0.12;te.gross_r=0.14;te.cost_r=0.02;te.observation_hash=SF12_DeriveFoldObservationHash(te);if(!engine.Observe(te,error)){Print(error);return INIT_FAILED;}
   }
   SF12_PromotionThresholds t;t.minimum_oos_folds=4;t.minimum_oos_samples=4;t.minimum_positive_fold_share=0.5;t.minimum_worst_fold_mean_r=0.0;t.minimum_oos_to_is_ratio=0.3;t.maximum_pbo=0.45;t.minimum_deflated_probability=0.90;t.maximum_reality_check_p=0.10;t.minimum_surface_support=0.40;t.minimum_best_trade_removed_mean_r=0.0;t.minimum_stress_floor_mean_r=0.0;
   SF12_ExternalDiagnostics x;x.probability_of_backtest_overfitting=0.20;x.deflated_probability=0.98;x.reality_check_p=0.02;x.surface_support=0.70;x.stress_floor_mean_r=0.03;x.diagnostics_hash="diagnostics_hash";
   SF12_PromotionDecision d;if(!engine.Finalize("decision_selftest",p.plan_hash,"trial_a",t,x,d,error)||d.status!=SF12_PROMOTION_ELIGIBLE_FOR_DATASET_REVIEW){Print("SF12 decision failed: ",error," reasons=",d.rejection_reasons);return INIT_FAILED;}
   Print("SF12 self-test PASS folds=",ArraySize(folds)," decision=",d.decision_hash);return INIT_SUCCEEDED;
}
void OnTick(){}
