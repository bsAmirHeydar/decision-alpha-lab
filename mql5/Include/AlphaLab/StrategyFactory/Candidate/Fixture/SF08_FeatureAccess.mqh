#ifndef __SF08_FEATURE_ACCESS_MQH__
#define __SF08_FEATURE_ACCESS_MQH__
#include "../SF08_TradeCandidate.mqh"
bool SF08_GetNumericFeature(const CSF01FeatureSnapshot &snapshot,const string feature_id,double &value,string &error)
{
   SF01_FeatureValue f;if(!snapshot.Get(feature_id,f)){error="required feature missing: "+feature_id;return false;}
   if(f.quality!=SF01_QUALITY_VALID && f.quality!=SF01_QUALITY_ESTIMATED){error="required feature not valid: "+feature_id;return false;}
   if(f.value_type==SF01_FEATURE_DOUBLE)value=f.double_value;
   else if(f.value_type==SF01_FEATURE_INTEGER)value=(double)f.integer_value;
   else if(f.value_type==SF01_FEATURE_BOOLEAN)value=f.boolean_value?1.0:0.0;
   else{error="feature is not numeric-compatible: "+feature_id;return false;}
   if(!MathIsValidNumber(value)){error="feature is non-finite: "+feature_id;return false;}error="";return true;
}
#endif
