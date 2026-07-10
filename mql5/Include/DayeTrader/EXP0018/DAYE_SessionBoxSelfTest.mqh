#ifndef __EXP0018_DAYE_SESSION_BOX_SELF_TEST_MQH__
#define __EXP0018_DAYE_SESSION_BOX_SELF_TEST_MQH__

#include <DayeTrader/EXP0018/DAYE_SessionBoxAudit.mqh>

bool DAYE_RunEmbeddedSessionBoxSelfTests(void)
{
   DAYE_SessionBoxConfig config;
   ZeroMemory(config);
   config.schema_version=DAYE_SESSION_BOX_SCHEMA_VERSION;
   config.lookback_weeks=2;
   config.render_session_a=true; config.render_session_l=true; config.render_session_n=true; config.render_session_p=true;
   config.render_complete_sessions=true; config.render_open_sessions=true; config.render_partial_sessions=false;
   config.require_symbol_period_publishable=false;
   config.fill_alpha=45; config.border_width=1; config.maximum_target_charts_per_symbol=8;
   config.object_verification_interval_seconds=10; config.maximum_projection_records=1000;
   config.period_config.include_session_periods=true;
   config.period_config.include_weekly_periods=false;
   string reason="";
   if(!DAYE_ValidateSessionBoxConfig(config,reason)) { Print("P09 selftest config failed ",reason); return false; }
   if(!DAYE_IsCanonicalSessionCode("A") || !DAYE_IsCanonicalSessionCode("P") || DAYE_IsCanonicalSessionCode("D")) return false;
   if(DAYE_BuildSessionBoxObjectName("snapshot-x")!=DAYE_BuildSessionBoxObjectName("snapshot-x")) return false;
   if(DAYE_BuildSessionBoxObjectName("snapshot-x")==DAYE_BuildSessionBoxObjectName("snapshot-y")) return false;

   DAYE_SymbolPeriodSnapshot snapshot;
   ZeroMemory(snapshot);
   snapshot.period_family=DAYE_FAMILY_SESSION;
   snapshot.period_code="N";
   snapshot.is_publishable=true;
   snapshot.completeness=DAYE_PERIOD_COMPLETENESS_COMPLETE;
   snapshot.observed_bar_count=360;
   snapshot.window.start_utc=100000;
   snapshot.window.end_utc=121600;
   snapshot.high=101.0; snapshot.low=99.0;
   DAYE_SessionBoxProjectionStatus status;
   if(!DAYE_IsSessionSnapshotEligible(snapshot,config,0,status,reason)) return false;
   snapshot.completeness=DAYE_PERIOD_COMPLETENESS_PARTIAL;
   if(DAYE_IsSessionSnapshotEligible(snapshot,config,0,status,reason)) return false;
   snapshot.completeness=DAYE_PERIOD_COMPLETENESS_OPEN;
   if(!DAYE_IsSessionSnapshotEligible(snapshot,config,0,status,reason)) return false;
   return true;
}

#endif
