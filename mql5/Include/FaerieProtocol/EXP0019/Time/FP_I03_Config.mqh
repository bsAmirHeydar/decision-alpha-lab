#ifndef __EXP0019_FP_I03_CONFIG_MQH__
#define __EXP0019_FP_I03_CONFIG_MQH__

#include <FaerieProtocol/EXP0019/Core/FP_I02_Hash.mqh>
#include "FP_I03_Types.mqh"

string FP_I03_ConfigMaterial(const FP_I03_TimeKernelConfig &config)
  {
   return config.context_id+"|"+config.timezone_name+"|"+config.time_rule_version+"|"+
          config.calendar_version+"|"+config.session_registry_version+"|"+
          IntegerToString(config.minimum_supported_year)+"|"+IntegerToString(config.maximum_supported_year)+"|"+
          IntegerToString((int)config.ambiguous_start_policy)+"|"+IntegerToString((int)config.ambiguous_end_policy);
  }

void FP_I03_DefaultConfig(FP_I03_TimeKernelConfig &config)
  {
   config.context_id="FP-CONTEXT-001";
   config.timezone_name=FP_I03_TIMEZONE;
   config.time_rule_version=FP_I03_TIME_RULE_VERSION;
   config.calendar_version=FP_I03_CALENDAR_VERSION;
   config.session_registry_version=FP_I03_SESSION_REGISTRY_VERSION;
   config.minimum_supported_year=FP_I03_MIN_YEAR;
   config.maximum_supported_year=FP_I03_MAX_YEAR;
   config.ambiguous_start_policy=FP_I03_LOCAL_EARLIEST;
   config.ambiguous_end_policy=FP_I03_LOCAL_LATEST;
   config.config_hash=FP_I02_SHA256(FP_I03_ConfigMaterial(config));
  }

bool FP_I03_ValidateConfig(const FP_I03_TimeKernelConfig &config,string &reason)
  {
   reason="";
   if(config.context_id!="FP-CONTEXT-001") {reason="FP_TRC_CONTEXT_ID_INVALID";return false;}
   if(config.timezone_name!=FP_I03_TIMEZONE) {reason="FP_TRC_TIMEZONE_UNSUPPORTED";return false;}
   if(config.minimum_supported_year<2007 || config.maximum_supported_year<config.minimum_supported_year) {reason="FP_TRC_YEAR_RANGE_INVALID";return false;}
   if(config.config_hash!=FP_I02_SHA256(FP_I03_ConfigMaterial(config))) {reason="FP_TRC_CONFIG_HASH_MISMATCH";return false;}
   return true;
  }

#endif
