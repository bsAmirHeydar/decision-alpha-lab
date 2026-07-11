#ifndef __SF12_VALIDATION_PLAN_MQH__
#define __SF12_VALIDATION_PLAN_MQH__
#include "SF12_ValidationEnums.mqh"
#include "../Statistics/SF11_AllStatistics.mqh"
struct SF12_ValidationPlan
{
   string schema;string plan_id;string plan_version;ENUM_SF12_SPLIT_METHOD method;
   string source_run_id;string source_manifest_hash;string source_artifact_hash;string strategy_id;string search_space_hash;
   long start_utc_msc;long end_utc_msc;long train_span_msc;long validation_span_msc;long test_span_msc;long step_span_msc;
   long purge_span_msc;long embargo_span_msc;int minimum_train_samples;int minimum_validation_samples;int minimum_test_samples;
   int maximum_folds;int random_seed;string plan_hash;
};
string SF12_ValidationPlanCanonical(const SF12_ValidationPlan &p)
{
   return p.schema+"|"+p.plan_id+"|"+p.plan_version+"|"+IntegerToString((int)p.method)+"|"+p.source_run_id+"|"+
      p.source_manifest_hash+"|"+p.source_artifact_hash+"|"+p.strategy_id+"|"+p.search_space_hash+"|"+
      IntegerToString(p.start_utc_msc)+"|"+IntegerToString(p.end_utc_msc)+"|"+IntegerToString(p.train_span_msc)+"|"+
      IntegerToString(p.validation_span_msc)+"|"+IntegerToString(p.test_span_msc)+"|"+IntegerToString(p.step_span_msc)+"|"+
      IntegerToString(p.purge_span_msc)+"|"+IntegerToString(p.embargo_span_msc)+"|"+IntegerToString(p.minimum_train_samples)+"|"+
      IntegerToString(p.minimum_validation_samples)+"|"+IntegerToString(p.minimum_test_samples)+"|"+IntegerToString(p.maximum_folds)+"|"+
      IntegerToString(p.random_seed);
}
string SF12_DeriveValidationPlanHash(const SF12_ValidationPlan &p){return SF01_StableId("vplan",SF12_ValidationPlanCanonical(p));}
bool SF12_ValidatePlan(const SF12_ValidationPlan &p,string &error)
{
   if(p.schema!="alpha_lab.strategy_factory/validation_plan@1.0.0"){error="unsupported validation plan schema";return false;}
   if(!SF01_IsSafeIdentifier(p.plan_id,128)||!SF01_IsSafeIdentifier(p.source_run_id,128)||!SF01_IsSafeIdentifier(p.strategy_id,128)||
      p.source_manifest_hash==""||p.source_artifact_hash==""||p.search_space_hash==""){error="missing validation plan lineage";return false;}
   if(p.end_utc_msc<=p.start_utc_msc||p.train_span_msc<=0||p.validation_span_msc<=0||p.test_span_msc<=0||p.step_span_msc<=0||
      p.purge_span_msc<0||p.embargo_span_msc<0||p.minimum_train_samples<1||p.minimum_validation_samples<1||p.minimum_test_samples<1||
      p.maximum_folds<1||p.maximum_folds>4096){error="invalid validation plan bounds";return false;}
   if(p.plan_hash!=""&&p.plan_hash!=SF12_DeriveValidationPlanHash(p)){error="validation plan hash mismatch";return false;}
   error="";return true;
}
#endif
