#property strict
#include <AlphaLab/StrategyFactory/Validation/SF12_AllValidation.mqh>
input int InpTrainDays=180;
input int InpValidationDays=30;
input int InpTestDays=30;
input int InpStepDays=30;
int OnInit()
{
   const long day=86400000;SF12_ValidationPlan p;p.schema="alpha_lab.strategy_factory/validation_plan@1.0.0";p.plan_id="sf12_diagnostic";p.plan_version="1.0.0";p.method=SF12_SPLIT_ROLLING_WALK_FORWARD;
   p.source_run_id="diagnostic_run";p.source_manifest_hash="diagnostic_manifest";p.source_artifact_hash="diagnostic_artifact";p.strategy_id="diagnostic_strategy";p.search_space_hash="diagnostic_search";
   p.start_utc_msc=0;p.end_utc_msc=(long)1000*day;p.train_span_msc=(long)InpTrainDays*day;p.validation_span_msc=(long)InpValidationDays*day;p.test_span_msc=(long)InpTestDays*day;p.step_span_msc=(long)InpStepDays*day;p.purge_span_msc=day;p.embargo_span_msc=day;
   p.minimum_train_samples=100;p.minimum_validation_samples=20;p.minimum_test_samples=20;p.maximum_folds=64;p.random_seed=120012;p.plan_hash=SF12_DeriveValidationPlanHash(p);SF12_ValidationFold folds[];string error;CSF12FoldCompiler c;
   if(!c.Compile(p,folds,error)){Print("SF12 diagnostic failed: ",error);return INIT_FAILED;}Print("SF12 diagnostic folds=",ArraySize(folds)," plan=",p.plan_hash);return INIT_SUCCEEDED;
}
void OnTick(){}
