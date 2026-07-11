#ifndef __SF13_FEATURE_COLUMN_MQH__
#define __SF13_FEATURE_COLUMN_MQH__
#include "SF13_TrainingEnums.mqh"
#include "../Contracts/SF01_AllContracts.mqh"
struct SF13_FeatureColumn{string feature_id;string feature_version;int ordinal;string value_type;bool required;string source_schema;string description;string column_hash;};
string SF13_FeatureColumnCanonical(const SF13_FeatureColumn &v){return "alpha_lab.strategy_factory/dataset_feature_column@1.0.0|"+v.feature_id+"|"+v.feature_version+"|"+IntegerToString(v.ordinal)+"|"+v.value_type+"|"+SF01_CanonicalBool(v.required)+"|"+v.source_schema+"|"+v.description;}
string SF13_DeriveFeatureColumnHash(const SF13_FeatureColumn &v){return SF01_StableId("fcol",SF13_FeatureColumnCanonical(v));}
bool SF13_ValidateFeatureColumn(const SF13_FeatureColumn &v,string &error){if(!SF01_IsSafeIdentifier(v.feature_id,160)||v.feature_version==""||v.ordinal<0||v.ordinal>=4096||v.value_type==""||v.source_schema==""){error="invalid feature column";return false;}if(v.column_hash!=""&&v.column_hash!=SF13_DeriveFeatureColumnHash(v)){error="feature column hash mismatch";return false;}error="";return true;}
#endif
