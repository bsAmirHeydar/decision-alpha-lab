#property strict
#property version   "2.11"
#property description "EXP0018 P11 deterministic chronological historical replay. No trading authority."

#include <DayeTrader/EXP0018/DAYE_ReplayEngine.mqh>

input group "EXP0018 P11 — Replay Range (New York wall time)"
input datetime InpReplayStartNewYork=D'2026.06.01 18:00:00';
input datetime InpReplayEndNewYork=D'2026.06.08 18:00:00';
input int InpMaximumReplayBars=20000;
input int InpCursorStepsPerTimer=10;
input int InpTimerSeconds=1;
input int InpProgressLogEverySteps=250;

input group "EXP0018 P11 — Symbols and Timeframes"
input string InpSymbolA="SPXUSD";
input string InpSymbolB="NDXUSD";
input string InpCanonicalSymbolA="SPX";
input string InpCanonicalSymbolB="NDX";
input ENUM_TIMEFRAMES InpBaseTimeframe=PERIOD_M1;
input ENUM_TIMEFRAMES InpHostTimeframe=PERIOD_M30;

input group "EXP0018 P11 — Replay Strictness"
input bool InpRequireManualFixedBrokerOffset=true;
input bool InpRequireCompleteSourceAlignment=true;
input bool InpFailOnPartialPeriodSource=false;
input bool InpFailOnPipelineError=true;

input group "EXP0018 P11 — Source and Period Policy"
input bool InpIncludeDailyPeriods=true;
input bool InpIncludeSessionPeriods=true;
input bool InpIncludeSubcyclePeriods=true;
input bool InpIncludeWeeklyPeriods=false;
input bool InpIncludeOpenPeriods=true;
input bool InpPublishPartialPeriods=true;
input bool InpEnableMajorRelationships=true;
input bool InpEnableMinorRelationships=true;
input bool InpAllowOpenCurrentPeriods=true;
input bool InpAllowPartialCurrentPeriods=false;
input bool InpRequireCompleteReferencePeriods=true;
input bool InpEnableHighSide=true;
input bool InpEnableLowSide=true;
input bool InpEqualityCountsAsHunt=true;

input group "EXP0018 P11 — Lifecycle Policy"
input bool InpAllowRepeatAcrossNewOpportunitiesWhileProtectedSurvives=true;
input bool InpSuppressDuplicateExactOpportunity=true;
input bool InpRetireOnProtectedTouch=true;
input bool InpRetireOnDoubleHunt=true;
input bool InpRetireOnRoleSwitch=true;
input bool InpPreserveAcceptedUsesAfterRetirement=true;
input bool InpPublishRejectedUses=true;

input group "EXP0018 P11 — Capacity"
input int InpMaximumPeriods=5000;
input int InpMaximumResolutions=10000;
input int InpMaximumObservations=20000;
input int InpMaximumPendingCandidates=10000;
input int InpMaximumResults=30000;
input int InpMaximumFinalizedIds=50000;
input int InpMaximumReferences=20000;
input int InpMaximumUses=50000;
input int InpMaximumProcessedResults=50000;

input group "EXP0018 P11 — Time Adapter"
input DAYE_BrokerOffsetMode InpBrokerOffsetMode=DAYE_BROKER_OFFSET_MANUAL_FIXED;
input double InpBrokerUtcOffsetHours=3.0;
input DAYE_NyOffsetMode InpNewYorkOffsetMode=DAYE_NY_AUTO_US_DST;
input double InpManualNewYorkUtcOffsetHours=-5.0;
input DAYE_LocalResolutionPolicy InpAmbiguousStartPolicy=DAYE_LOCAL_EARLIEST;
input DAYE_LocalResolutionPolicy InpAmbiguousEndPolicy=DAYE_LOCAL_LATEST;

input group "EXP0018 P11 — Output"
input string InpOutputPrefix="EXP0018_Phase11_Replay_v2";
input bool InpWriteFrameRows=false;
input int InpFrameAuditStride=30;
input bool InpWriteEventRows=true;
input bool InpWriteConfirmationRows=true;
input bool InpWriteReferenceRows=true;
input bool InpWriteUseRows=true;
input bool InpRunEmbeddedSelfTestsOnInit=true;
input bool InpShowProgressInChartComment=true;

CDayeHistoricalReplayEngine g_replay;

void DAYE_BuildReplayTimeConfig(DAYE_TimeConfig &config)
{
   ZeroMemory(config); config.schema_version=DAYE_TIME_SCHEMA_VERSION;
   config.broker_offset_mode=InpBrokerOffsetMode;
   config.broker_utc_offset_minutes=(int)MathRound(InpBrokerUtcOffsetHours*60.0);
   config.ny_offset_mode=InpNewYorkOffsetMode;
   config.manual_new_york_utc_offset_minutes=(int)MathRound(InpManualNewYorkUtcOffsetHours*60.0);
   config.ambiguous_start_policy=InpAmbiguousStartPolicy; config.ambiguous_end_policy=InpAmbiguousEndPolicy;
}

void DAYE_BuildReplayConfig(DAYE_ReplayConfig &config)
{
   ZeroMemory(config); config.schema_version=DAYE_REPLAY_SCHEMA_VERSION;
   config.replay_start_new_york=InpReplayStartNewYork; config.replay_end_new_york=InpReplayEndNewYork;
   config.require_manual_fixed_broker_offset=InpRequireManualFixedBrokerOffset;
   config.require_complete_source_alignment=InpRequireCompleteSourceAlignment;
   config.fail_on_partial_period_source=InpFailOnPartialPeriodSource; config.fail_on_pipeline_error=InpFailOnPipelineError;
   config.maximum_replay_bars=InpMaximumReplayBars; config.cursor_steps_per_timer=InpCursorStepsPerTimer;
   config.progress_log_every_steps=InpProgressLogEverySteps; config.frame_audit_stride=InpFrameAuditStride;
   config.write_frame_rows=InpWriteFrameRows; config.write_event_rows=InpWriteEventRows;
   config.write_confirmation_rows=InpWriteConfirmationRows; config.write_reference_rows=InpWriteReferenceRows;
   config.write_use_rows=InpWriteUseRows; config.output_prefix=InpOutputPrefix;

   config.lifecycle_config.schema_version=DAYE_LIFECYCLE_SCHEMA_VERSION;
   config.lifecycle_config.confirmation_config.schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION;
   config.lifecycle_config.confirmation_config.hunt_config.schema_version=DAYE_HUNT_SCHEMA_VERSION;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.schema_version=DAYE_RELATIONSHIP_SCHEMA_VERSION;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.schema_version=DAYE_PERIOD_AGG_SCHEMA_VERSION;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.schema_version=DAYE_DATA_SCHEMA_VERSION;

   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.broker_symbol_a=InpSymbolA;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.broker_symbol_b=InpSymbolB;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_a=InpCanonicalSymbolA;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_b=InpCanonicalSymbolB;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.base_timeframe=InpBaseTimeframe;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.requested_bars_per_symbol=InpMaximumReplayBars;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.minimum_common_bars=1;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.maximum_pairs_to_publish=InpMaximumReplayBars;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.use_closed_bars_only=true;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.require_series_synchronized=false;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.fail_on_any_invalid_bar=true;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.require_complete_alignment=InpRequireCompleteSourceAlignment;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.enforce_freshness=false;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.maximum_latest_bar_age_seconds=0;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.force_full_refresh_seconds=0;

   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.include_daily_periods=InpIncludeDailyPeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.include_session_periods=InpIncludeSessionPeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.include_subcycle_periods=InpIncludeSubcyclePeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.include_weekly_periods=InpIncludeWeeklyPeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.include_open_periods=InpIncludeOpenPeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.publish_partial_periods=InpPublishPartialPeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.require_both_symbols_complete=false;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.minimum_publishable_coverage_percent=0.0;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.minimum_complete_paired_periods=0;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.maximum_periods_to_publish=InpMaximumPeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.force_full_refresh_seconds=0;

   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.enable_major_relationships=InpEnableMajorRelationships;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.enable_minor_relationships=InpEnableMinorRelationships;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.allow_open_current_periods=InpAllowOpenCurrentPeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.allow_partial_current_periods=InpAllowPartialCurrentPeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.require_complete_reference_periods=InpRequireCompleteReferencePeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.publish_unavailable_resolutions=false;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.publish_blocked_registry_records=false;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.minimum_ready_resolutions=0;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.maximum_resolutions_to_publish=InpMaximumResolutions;

   config.lifecycle_config.confirmation_config.hunt_config.enable_high_side=InpEnableHighSide;
   config.lifecycle_config.confirmation_config.hunt_config.enable_low_side=InpEnableLowSide;
   config.lifecycle_config.confirmation_config.hunt_config.equality_counts_as_hunt=InpEqualityCountsAsHunt;
   config.lifecycle_config.confirmation_config.hunt_config.publish_unavailable_observations=false;
   config.lifecycle_config.confirmation_config.hunt_config.require_positive_prices=true;
   config.lifecycle_config.confirmation_config.hunt_config.minimum_ready_observations=0;
   config.lifecycle_config.confirmation_config.hunt_config.maximum_observations_to_publish=InpMaximumObservations;

   config.lifecycle_config.confirmation_config.host_timeframe=InpHostTimeframe;
   config.lifecycle_config.confirmation_config.require_exact_host_symbol_alignment=true;
   config.lifecycle_config.confirmation_config.require_closed_host_bars=true;
   config.lifecycle_config.confirmation_config.persist_checkpoint=false;
   config.lifecycle_config.confirmation_config.checkpoint_prefix="EXP0018_P11_NO_LIVE_CHECKPOINT";
   config.lifecycle_config.confirmation_config.publish_nonconfirmed_results=true;
   config.lifecycle_config.confirmation_config.fail_closed_on_missed_host_close=true;
   config.lifecycle_config.confirmation_config.maximum_pending_candidates=InpMaximumPendingCandidates;
   config.lifecycle_config.confirmation_config.maximum_results_to_publish=InpMaximumResults;
   config.lifecycle_config.confirmation_config.maximum_finalized_ids_to_remember=InpMaximumFinalizedIds;

   config.lifecycle_config.allow_repeat_across_new_opportunities_while_protected_survives=InpAllowRepeatAcrossNewOpportunitiesWhileProtectedSurvives;
   config.lifecycle_config.suppress_duplicate_exact_opportunity=InpSuppressDuplicateExactOpportunity;
   config.lifecycle_config.retire_on_protected_touch=InpRetireOnProtectedTouch;
   config.lifecycle_config.retire_on_double_hunt=InpRetireOnDoubleHunt;
   config.lifecycle_config.retire_on_role_switch=InpRetireOnRoleSwitch;
   config.lifecycle_config.preserve_accepted_uses_after_retirement=InpPreserveAcceptedUsesAfterRetirement;
   config.lifecycle_config.publish_rejected_uses=InpPublishRejectedUses;
   config.lifecycle_config.persist_checkpoint=false;
   config.lifecycle_config.checkpoint_prefix="EXP0018_P11_NO_LIVE_CHECKPOINT";
   config.lifecycle_config.maximum_reference_records=InpMaximumReferences;
   config.lifecycle_config.maximum_use_records=InpMaximumUses;
   config.lifecycle_config.maximum_processed_result_ids=InpMaximumProcessedResults;
}

int OnInit()
{
   DAYE_TimeConfig time_config; DAYE_ReplayConfig replay_config;
   DAYE_BuildReplayTimeConfig(time_config); DAYE_BuildReplayConfig(replay_config);
   if(!g_replay.Initialize(replay_config,time_config,InpRunEmbeddedSelfTestsOnInit)) return INIT_FAILED;
   EventSetTimer(MathMax(1,InpTimerSeconds));
   return INIT_SUCCEEDED;
}

void OnTimer()
{
   g_replay.ProcessChunk(MathMax(1,InpCursorStepsPerTimer));
   DAYE_ReplaySummary summary;
   if(g_replay.GetSummary(summary))
   {
      if(InpShowProgressInChartComment)
         Comment("EXP0018 P11 Historical Replay\n",DAYE_ReplayStatusToString(summary.status),"\n",
                 summary.processed_cursor_count," / ",summary.cursor_count," cursors\n",
                 "confirmed=",summary.confirmed_count," accepted=",summary.accepted_use_count," retired=",summary.retired_reference_count,"\n",
                 "state_hash=",summary.final_state_hash,"\nNo trading authority.");
      if(summary.status==DAYE_REPLAY_STATUS_COMPLETE || summary.status==DAYE_REPLAY_STATUS_PIPELINE_FAILED)
         EventKillTimer();
   }
}

void OnDeinit(const int reason)
{
   EventKillTimer(); Comment(""); g_replay.Shutdown();
}

void OnTick() {}
