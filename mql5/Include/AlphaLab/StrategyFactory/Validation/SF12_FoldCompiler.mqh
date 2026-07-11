#ifndef __SF12_FOLD_COMPILER_MQH__
#define __SF12_FOLD_COMPILER_MQH__
#include "SF12_ValidationFold.mqh"
class CSF12FoldCompiler
{
public:
   bool Compile(const SF12_ValidationPlan &input_plan,SF12_ValidationFold &folds[],string &error) const
   {
      SF12_ValidationPlan plan=input_plan;if(!SF12_ValidatePlan(plan,error))return false;if(plan.plan_hash=="")plan.plan_hash=SF12_DeriveValidationPlanHash(plan);
      if(plan.method!=SF12_SPLIT_ANCHORED_WALK_FORWARD&&plan.method!=SF12_SPLIT_ROLLING_WALK_FORWARD){error="MQL5 fold compiler supports walk-forward plans";return false;}
      ArrayResize(folds,0);long anchor=plan.start_utc_msc+plan.train_span_msc;
      for(int ordinal=0;ordinal<plan.maximum_folds;ordinal++)
      {
         const long train_start=(plan.method==SF12_SPLIT_ANCHORED_WALK_FORWARD)?plan.start_utc_msc:anchor-plan.train_span_msc;
         const long train_end=anchor;const long validation_start=train_end+plan.purge_span_msc;const long validation_end=validation_start+plan.validation_span_msc;
         const long test_start=validation_end+plan.embargo_span_msc;const long test_end=test_start+plan.test_span_msc;if(test_end>plan.end_utc_msc)break;
         SF12_ValidationFold f;f.schema="alpha_lab.strategy_factory/validation_fold@1.0.0";f.ordinal=ordinal;f.plan_hash=plan.plan_hash;
         f.fold_id=SF01_StableId("fold",plan.plan_hash+"|"+IntegerToString(ordinal)+"|"+IntegerToString(train_start)+"|"+IntegerToString(test_end));
         f.train.start_utc_msc=train_start;f.train.end_utc_msc=train_end;f.purge_before_validation.start_utc_msc=train_end;f.purge_before_validation.end_utc_msc=validation_start;
         f.validation.start_utc_msc=validation_start;f.validation.end_utc_msc=validation_end;f.embargo_before_test.start_utc_msc=validation_end;f.embargo_before_test.end_utc_msc=test_start;
         f.test.start_utc_msc=test_start;f.test.end_utc_msc=test_end;f.fold_hash="";f.fold_hash=SF12_DeriveValidationFoldHash(f);
         const int n=ArraySize(folds);ArrayResize(folds,n+1);folds[n]=f;anchor+=plan.step_span_msc;
      }
      if(ArraySize(folds)==0){error="validation horizon cannot produce a complete fold";return false;}error="";return true;
   }
};
#endif
