#ifndef __EXP0019_FP_I02_VALIDATION_MQH__
#define __EXP0019_FP_I02_VALIDATION_MQH__

#include "FP_I02_Config.mqh"
#include "FP_I02_Relations.mqh"
#include "FP_I02_StateMachines.mqh"

bool FP_I02_ValidateWindowKey(const FP_I02_WindowKey &value,string &reason_code)
  {
   reason_code=FP_RC_WINDOW_INTERVAL_INVALID;
   if(value.context_id!=FP_I02_CONTEXT_ID || value.pair_id=="" || value.trading_day_id=="" || value.timezone=="") return false;
   if(value.start_utc_ms<0 || value.end_utc_ms<=value.start_utc_ms) return false;
   if(value.scope==FP_SCOPE_EXACT_PRIOR_CALENDAR_OFFSET && value.calendar_offset<=0) return false;
   if(value.scope!=FP_SCOPE_EXACT_PRIOR_CALENDAR_OFFSET && value.calendar_offset!=0) return false;
   if(value.kind==FP_WINDOW_W && value.week_id=="") return false;
   reason_code=FP_RC_READY;
   return true;
  }

bool FP_I02_ValidateManifest(const FP_I02_ContextManifest &value,string &reason_code)
  {
   reason_code=FP_RC_INVALID_CONFIG;
   if(value.schema_version!=FP_I02_SCHEMA_VERSION || value.context_id!=FP_I02_CONTEXT_ID || value.context_version!=FP_I02_CONTEXT_VERSION) return false;
   if(value.decision_set_id!=FP_I02_DECISION_SET_ID || value.resolved_confirmation_timeframe_seconds<=0) return false;
   if(!FP_I02_IsLowerSha256(value.semantic_config_hash) || !FP_I02_IsLowerSha256(value.projection_config_hash) || !FP_I02_IsLowerSha256(value.dependency_snapshot_hash)) { reason_code=FP_RC_INVALID_SHA256; return false; }
   if(value.execution_authority==FP_AUTHORITY_LIVE && StringFind(value.open_decision_ids,"FP-DEC-012")>=0) { reason_code=FP_RC_OPEN_DECISION_BLOCKS_LIVE; return false; }
   reason_code=FP_RC_READY;
   return true;
  }

#endif
