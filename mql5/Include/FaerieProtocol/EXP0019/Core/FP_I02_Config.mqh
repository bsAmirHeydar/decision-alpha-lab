#ifndef __EXP0019_FP_I02_CONFIG_MQH__
#define __EXP0019_FP_I02_CONFIG_MQH__

#include "FP_I02_Types.mqh"
#include "FP_I02_Hash.mqh"

struct FP_I02_SemanticConfig
  {
   string decision_set_id;
   string primary_symbol;
   string secondary_symbol;
   string timezone;
   int resolved_confirmation_timeframe_seconds;
   int historical_n_depth;
   bool replace_missing_offsets;
   FP_I02_QuotaConsumptionPolicy quota_consumption_policy;
   string source_data_revision;
   string adapter_snapshot_hash;
   string semantic_config_hash;
  };

struct FP_I02_ProjectionConfig
  {
   int line_width;
   int active_opacity;
   int suppressed_opacity;
   bool show_session_boxes;
   bool show_reference_levels;
   bool show_hunt_markers;
   bool show_candidate_lines;
   bool show_confirmed_signals;
   bool show_ww_context;
   bool show_health_panel;
   int label_font_size;
   string projection_config_hash;
  };

bool FP_I02_ValidateSemanticConfig(const FP_I02_SemanticConfig &config,string &reason_code)
  {
   reason_code=FP_RC_INVALID_CONFIG;
   if(config.decision_set_id!=FP_I02_DECISION_SET_ID) return false;
   if(config.primary_symbol=="" || config.secondary_symbol=="" || config.primary_symbol==config.secondary_symbol) { reason_code=FP_RC_SYMBOL_PAIR_INVALID; return false; }
   if(config.timezone!="America/New_York") return false;
   if(config.resolved_confirmation_timeframe_seconds<=0 || config.historical_n_depth<=0) return false;
   if(config.replace_missing_offsets) return false;
   if(!FP_I02_IsLowerSha256(config.adapter_snapshot_hash)) { reason_code=FP_RC_INVALID_SHA256; return false; }
   if(config.source_data_revision=="") return false;
   reason_code=FP_RC_READY;
   return true;
  }

bool FP_I02_ValidateProjectionConfig(const FP_I02_ProjectionConfig &config,string &reason_code)
  {
   reason_code=FP_RC_INVALID_CONFIG;
   if(config.line_width<1 || config.line_width>5) return false;
   if(config.active_opacity<0 || config.active_opacity>255 || config.suppressed_opacity<0 || config.suppressed_opacity>255) return false;
   if(config.label_font_size<6 || config.label_font_size>30) return false;
   reason_code=FP_RC_READY;
   return true;
  }

FP_I02_ExecutionAuthority FP_I02_ResolveAuthority(const FP_I02_ContextProfile profile,const FP_I02_QuotaConsumptionPolicy quota_policy)
  {
   if(profile==FP_PROFILE_CANONICAL_PAPER) return FP_AUTHORITY_PAPER_ONLY;
   if(profile==FP_PROFILE_CANONICAL_LIVE && quota_policy!=FP_QUOTA_POLICY_UNSET) return FP_AUTHORITY_LIVE;
   return FP_AUTHORITY_NONE;
  }

#endif
