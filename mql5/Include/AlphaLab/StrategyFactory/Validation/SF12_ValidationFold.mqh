#ifndef __SF12_VALIDATION_FOLD_MQH__
#define __SF12_VALIDATION_FOLD_MQH__
#include "SF12_ValidationPlan.mqh"
struct SF12_TimeRange{long start_utc_msc;long end_utc_msc;};
struct SF12_ValidationFold
{
   string schema;string fold_id;int ordinal;string plan_hash;SF12_TimeRange train;SF12_TimeRange validation;SF12_TimeRange test;
   SF12_TimeRange purge_before_validation;SF12_TimeRange embargo_before_test;string fold_hash;
};
bool SF12_TimeRangeContains(const SF12_TimeRange &r,const long timestamp_utc_msc){return timestamp_utc_msc>=r.start_utc_msc&&timestamp_utc_msc<r.end_utc_msc;}
string SF12_ValidationFoldCanonical(const SF12_ValidationFold &f)
{
   return f.schema+"|"+f.fold_id+"|"+IntegerToString(f.ordinal)+"|"+f.plan_hash+"|"+
      IntegerToString(f.train.start_utc_msc)+"|"+IntegerToString(f.train.end_utc_msc)+"|"+
      IntegerToString(f.validation.start_utc_msc)+"|"+IntegerToString(f.validation.end_utc_msc)+"|"+
      IntegerToString(f.test.start_utc_msc)+"|"+IntegerToString(f.test.end_utc_msc)+"|"+
      IntegerToString(f.purge_before_validation.start_utc_msc)+"|"+IntegerToString(f.purge_before_validation.end_utc_msc)+"|"+
      IntegerToString(f.embargo_before_test.start_utc_msc)+"|"+IntegerToString(f.embargo_before_test.end_utc_msc);
}
string SF12_DeriveValidationFoldHash(const SF12_ValidationFold &f){return SF01_StableId("vfold",SF12_ValidationFoldCanonical(f));}
#endif
