#ifndef __EXP0018_DAYE_SESSION_BOX_POLICY_MQH__
#define __EXP0018_DAYE_SESSION_BOX_POLICY_MQH__

#include <DayeTrader/EXP0018/DAYE_SessionBoxIdentity.mqh>

bool DAYE_IsCanonicalSessionCode(const string code)
{
   return code=="A" || code=="L" || code=="N" || code=="P";
}

bool DAYE_IsSessionEnabled(const string code,const DAYE_SessionBoxConfig &config)
{
   if(code=="A") return config.render_session_a;
   if(code=="L") return config.render_session_l;
   if(code=="N") return config.render_session_n;
   if(code=="P") return config.render_session_p;
   return false;
}

color DAYE_SessionColor(const string code,const DAYE_SessionBoxConfig &config)
{
   if(code=="A") return config.color_a;
   if(code=="L") return config.color_l;
   if(code=="N") return config.color_n;
   return config.color_p;
}

bool DAYE_IsSessionSnapshotEligible(const DAYE_SymbolPeriodSnapshot &snapshot,
                                    const DAYE_SessionBoxConfig &config,
                                    const datetime lookback_start_utc,
                                    DAYE_SessionBoxProjectionStatus &status,
                                    string &reason_code)
{
   status=DAYE_SESSION_BOX_STATUS_UNKNOWN;
   reason_code="";
   if(snapshot.period_family!=DAYE_FAMILY_SESSION || !DAYE_IsCanonicalSessionCode(snapshot.period_code))
   {
      status=DAYE_SESSION_BOX_STATUS_SKIPPED_INELIGIBLE_COMPLETENESS;
      reason_code="not_a_canonical_session_period";
      return false;
   }
   if(!DAYE_IsSessionEnabled(snapshot.period_code,config))
   {
      status=DAYE_SESSION_BOX_STATUS_SKIPPED_DISABLED_SESSION;
      reason_code="session_disabled_by_input";
      return false;
   }
   if(snapshot.window.start_utc<lookback_start_utc)
   {
      status=DAYE_SESSION_BOX_STATUS_SKIPPED_OUTSIDE_LOOKBACK;
      reason_code="session_start_before_configured_lookback";
      return false;
   }
   if(config.require_symbol_period_publishable && !snapshot.is_publishable)
   {
      status=DAYE_SESSION_BOX_STATUS_SKIPPED_INELIGIBLE_COMPLETENESS;
      reason_code="symbol_period_not_publishable";
      return false;
   }
   if(snapshot.completeness==DAYE_PERIOD_COMPLETENESS_COMPLETE && config.render_complete_sessions) return true;
   if(snapshot.completeness==DAYE_PERIOD_COMPLETENESS_OPEN && config.render_open_sessions && snapshot.observed_bar_count>0) return true;
   if(snapshot.completeness==DAYE_PERIOD_COMPLETENESS_PARTIAL && config.render_partial_sessions && snapshot.observed_bar_count>0) return true;
   status=DAYE_SESSION_BOX_STATUS_SKIPPED_INELIGIBLE_COMPLETENESS;
   reason_code="session_completeness_not_admitted:"+DAYE_PeriodCompletenessToString(snapshot.completeness);
   return false;
}

bool DAYE_ValidateSessionBoxConfig(const DAYE_SessionBoxConfig &config,string &reason_code)
{
   reason_code="";
   if(config.schema_version!=DAYE_SESSION_BOX_SCHEMA_VERSION) { reason_code="session_box_schema_version_mismatch"; return false; }
   if(config.lookback_weeks<1 || config.lookback_weeks>104) { reason_code="lookback_weeks_out_of_range"; return false; }
   if(!config.render_session_a && !config.render_session_l && !config.render_session_n && !config.render_session_p)
   { reason_code="all_session_families_disabled"; return false; }
   if(!config.render_complete_sessions && !config.render_open_sessions && !config.render_partial_sessions)
   { reason_code="all_completeness_classes_disabled"; return false; }
   if(config.fill_alpha<0 || config.fill_alpha>255) { reason_code="fill_alpha_out_of_range"; return false; }
   if(config.border_width<1 || config.border_width>5) { reason_code="border_width_out_of_range"; return false; }
   if(config.maximum_target_charts_per_symbol<1 || config.maximum_target_charts_per_symbol>32)
   { reason_code="maximum_target_charts_per_symbol_out_of_range"; return false; }
   if(config.object_verification_interval_seconds<1 || config.object_verification_interval_seconds>3600)
   { reason_code="object_verification_interval_seconds_out_of_range"; return false; }
   if(config.maximum_projection_records<16 || config.maximum_projection_records>200000)
   { reason_code="maximum_projection_records_out_of_range"; return false; }
   if(!config.period_config.include_session_periods) { reason_code="period_config_must_include_sessions"; return false; }
   if(config.period_config.include_weekly_periods) { reason_code="weekly_periods_are_not_part_of_p09"; return false; }
   return true;
}

#endif
