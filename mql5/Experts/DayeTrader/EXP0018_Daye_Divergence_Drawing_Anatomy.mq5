#property strict
#property version   "2.00"
#property description "EXP0018 P08 immutable divergence-line projection on hunter-symbol charts. No trading authority."

#include <DayeTrader/EXP0018/DAYE_RenderEngine.mqh>
#include <AlphaLab/UC04/AL_UC04DayeTimeConfig.mqh>

input group "EXP0018 P08 — Symbols"
input string InpSymbolA="SPXUSD";
input string InpSymbolB="NDXUSD";
input string InpCanonicalSymbolA="SPX";
input string InpCanonicalSymbolB="NDX";

input group "EXP0018 P08 — Source and Host Timeframes"
input ENUM_TIMEFRAMES InpBaseTimeframe=PERIOD_M1;
input ENUM_TIMEFRAMES InpHostTimeframe=PERIOD_CURRENT;
input int InpRequestedBarsPerSymbol=10000;
input int InpMinimumCommonBars=500;
input int InpMaximumPairsToPublish=10000;
input int InpMinimumCompletePairedPeriods=10;
input int InpMaximumPeriodsToPublish=2000;
input int InpMaximumResolutionsToPublish=5000;
input int InpMaximumObservationsToPublish=10000;
input int InpMaximumPendingCandidates=5000;
input int InpMaximumConfirmationResults=10000;
input int InpMaximumFinalizedIds=20000;

input group "EXP0018 P08 — Core Source Policy"
input bool InpUseClosedBarsOnly=true;
input bool InpRequireSeriesSynchronized=true;
input bool InpFailOnAnyInvalidBar=true;
input bool InpRequireCompleteSourceAlignment=false;
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
input bool InpPublishUnavailableResolutions=true;
input bool InpPublishBlockedRegistryRecords=true;
input bool InpEnableHighSide=true;
input bool InpEnableLowSide=true;
input bool InpEqualityCountsAsHunt=true;
input bool InpPublishUnavailableObservations=false;
input bool InpRequirePositivePrices=true;
input bool InpRequireExactHostSymbolAlignment=true;
input bool InpRequireClosedHostBars=true;
input bool InpPublishNonconfirmedResults=true;
input bool InpFailClosedOnMissedHostClose=true;

input group "EXP0018 P08 — Lifecycle"
input bool InpAllowRepeatAcrossNewOpportunitiesWhileProtectedSurvives=true;
input bool InpSuppressDuplicateExactOpportunity=true;
input bool InpRetireOnProtectedTouch=true;
input bool InpRetireOnDoubleHunt=true;
input bool InpRetireOnRoleSwitch=true;
input bool InpPreserveAcceptedUsesAfterRetirement=true;
input bool InpPublishRejectedUses=true;
input int InpMaximumReferenceRecords=10000;
input int InpMaximumUseRecords=20000;
input int InpMaximumProcessedResultIds=30000;
input bool InpPersistConfirmationCheckpoint=true;
input string InpConfirmationCheckpointPrefix="EXP0018_P06_Confirmation_State_v2";
input bool InpPersistLifecycleCheckpoint=true;
input string InpLifecycleCheckpointPrefix="EXP0018_P07_Lifecycle_State_v2";

input group "EXP0018 P08 — Target Charts"
input DAYE_RenderTargetPolicy InpTargetChartPolicy=DAYE_RENDER_TARGET_ALL_OPEN_HUNTER_CHARTS;
input bool InpRequireTargetChartHostTimeframe=false;
input bool InpOpenMissingHunterChart=false;
input ENUM_TIMEFRAMES InpOpenedChartTimeframe=PERIOD_CURRENT;
input int InpMaximumTargetChartsPerUse=16;

input group "EXP0018 P08 — Trend Line"
input color InpDivergenceLineColor=clrTomato;
input ENUM_LINE_STYLE InpDivergenceLineStyle=STYLE_SOLID;
input int InpDivergenceLineWidth=2;
input bool InpRayLeft=false;
input bool InpRayRight=false;
input bool InpDrawInBackground=false;
input bool InpObjectsSelectable=false;
input bool InpObjectsHidden=false;
input DAYE_ExtremeAnchorPolicy InpReferenceExtremeAnchor=DAYE_EXTREME_ANCHOR_FIRST_OCCURRENCE;

input group "EXP0018 P08 — Major Signal Labels"
input bool InpShowMajorSignalLabels=true;
input bool InpUseMidpointTextObject=true;
input string InpLabelFont="Arial";
input int InpLabelFontSize=9;
input color InpLabelColor=clrTomato;
input double InpLabelVerticalOffsetPoints=10.0;

input group "EXP0018 P08 — Idempotency and Persistence"
input bool InpVerifyExistingOwnedObjects=true;
input bool InpRepairExistingOwnedObjects=true;
input bool InpRecreateManuallyDeletedOwnedObjects=true;
input bool InpPreserveOrphanedOwnedObjects=true;
input bool InpDeleteOwnedObjectsOnDeinit=false;
input int InpMaximumProjectionRecords=30000;

input group "EXP0018 P08 — Refresh"
input bool InpEnforceSourceFreshness=false;
input int InpMaximumLatestBarAgeSeconds=300;
input int InpForceFullRefreshSeconds=60;
input int InpTimerSeconds=1;

input group "EXP0018 P08 — Time Adapter"
input DAYE_BrokerOffsetMode InpBrokerOffsetMode=DAYE_BROKER_OFFSET_MANUAL_FIXED;
input double InpBrokerUtcOffsetHours=3.0;
input DAYE_NyOffsetMode InpNewYorkOffsetMode=DAYE_NY_AUTO_US_DST;
input double InpManualNewYorkUtcOffsetHours=-5.0;
input DAYE_LocalResolutionPolicy InpAmbiguousStartPolicy=DAYE_LOCAL_EARLIEST;
input DAYE_LocalResolutionPolicy InpAmbiguousEndPolicy=DAYE_LOCAL_LATEST;

input group "EXP0018 P08 — Diagnostics"
input bool InpRunEmbeddedSelfTestsOnInit=true;
input bool InpPrintSummaryOnRefresh=true;
input bool InpPrintLatestProjection=true;
input bool InpPrintTransitionEvents=true;
input bool InpShowChartComment=false;

input group "EXP0018 P08 — Optional Audit"
input bool InpWriteAuditCsv=false;
input bool InpWriteSummaryRows=true;
input int InpAuditLatestProjectionCount=25;
input string InpAuditCsvFilename="EXP0018_Phase08_Divergence_Drawing_Audit_v2.csv";

CDayeRenderEngine g_daye_render_engine;

void DAYE_BuildP08TimeConfig(DAYE_TimeConfig &config)
{
   AL_UC04BuildDayeTimeConfig(
      config,
      InpBrokerOffsetMode,
      InpBrokerUtcOffsetHours,
      InpNewYorkOffsetMode,
      InpManualNewYorkUtcOffsetHours,
      InpAmbiguousStartPolicy,
      InpAmbiguousEndPolicy
   );
}

void DAYE_BuildP08Config(DAYE_RenderConfig &config)
{
   ZeroMemory(config); config.schema_version=DAYE_RENDER_SCHEMA_VERSION;
   config.lifecycle_config.schema_version=DAYE_LIFECYCLE_SCHEMA_VERSION;
   config.lifecycle_config.confirmation_config.schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION;
   config.lifecycle_config.confirmation_config.hunt_config.schema_version=DAYE_HUNT_SCHEMA_VERSION;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.schema_version=DAYE_RELATIONSHIP_SCHEMA_VERSION;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.schema_version=DAYE_PERIOD_AGG_SCHEMA_VERSION;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.schema_version=DAYE_DATA_SCHEMA_VERSION;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.broker_symbol_a=InpSymbolA; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.broker_symbol_b=InpSymbolB;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_a=InpCanonicalSymbolA; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_b=InpCanonicalSymbolB;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.base_timeframe=InpBaseTimeframe; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.requested_bars_per_symbol=InpRequestedBarsPerSymbol;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.minimum_common_bars=InpMinimumCommonBars; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.maximum_pairs_to_publish=InpMaximumPairsToPublish;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.use_closed_bars_only=InpUseClosedBarsOnly; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.require_series_synchronized=InpRequireSeriesSynchronized;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.fail_on_any_invalid_bar=InpFailOnAnyInvalidBar; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.require_complete_alignment=InpRequireCompleteSourceAlignment;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.enforce_freshness=InpEnforceSourceFreshness; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.maximum_latest_bar_age_seconds=InpMaximumLatestBarAgeSeconds;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.force_full_refresh_seconds=InpForceFullRefreshSeconds;

   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.include_daily_periods=InpIncludeDailyPeriods; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.include_session_periods=InpIncludeSessionPeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.include_subcycle_periods=InpIncludeSubcyclePeriods; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.include_weekly_periods=InpIncludeWeeklyPeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.include_open_periods=InpIncludeOpenPeriods; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.publish_partial_periods=InpPublishPartialPeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.require_both_symbols_complete=false; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.minimum_publishable_coverage_percent=0.0;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.minimum_complete_paired_periods=InpMinimumCompletePairedPeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.maximum_periods_to_publish=InpMaximumPeriodsToPublish; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.force_full_refresh_seconds=InpForceFullRefreshSeconds;

   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.enable_major_relationships=InpEnableMajorRelationships; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.enable_minor_relationships=InpEnableMinorRelationships;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.allow_open_current_periods=InpAllowOpenCurrentPeriods; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.allow_partial_current_periods=InpAllowPartialCurrentPeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.require_complete_reference_periods=InpRequireCompleteReferencePeriods;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.publish_unavailable_resolutions=InpPublishUnavailableResolutions; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.publish_blocked_registry_records=InpPublishBlockedRegistryRecords;
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.minimum_ready_resolutions=1; config.lifecycle_config.confirmation_config.hunt_config.relationship_config.maximum_resolutions_to_publish=InpMaximumResolutionsToPublish;

   config.lifecycle_config.confirmation_config.hunt_config.enable_high_side=InpEnableHighSide; config.lifecycle_config.confirmation_config.hunt_config.enable_low_side=InpEnableLowSide;
   config.lifecycle_config.confirmation_config.hunt_config.equality_counts_as_hunt=InpEqualityCountsAsHunt;
   config.lifecycle_config.confirmation_config.hunt_config.publish_unavailable_observations=InpPublishUnavailableObservations;
   config.lifecycle_config.confirmation_config.hunt_config.require_positive_prices=InpRequirePositivePrices;
   config.lifecycle_config.confirmation_config.hunt_config.minimum_ready_observations=1; config.lifecycle_config.confirmation_config.hunt_config.maximum_observations_to_publish=InpMaximumObservationsToPublish;

   config.lifecycle_config.confirmation_config.host_timeframe=InpHostTimeframe; config.lifecycle_config.confirmation_config.require_exact_host_symbol_alignment=InpRequireExactHostSymbolAlignment;
   config.lifecycle_config.confirmation_config.require_closed_host_bars=InpRequireClosedHostBars; config.lifecycle_config.confirmation_config.persist_checkpoint=InpPersistConfirmationCheckpoint;
   config.lifecycle_config.confirmation_config.checkpoint_prefix=InpConfirmationCheckpointPrefix; config.lifecycle_config.confirmation_config.publish_nonconfirmed_results=InpPublishNonconfirmedResults;
   config.lifecycle_config.confirmation_config.fail_closed_on_missed_host_close=InpFailClosedOnMissedHostClose;
   config.lifecycle_config.confirmation_config.maximum_pending_candidates=InpMaximumPendingCandidates; config.lifecycle_config.confirmation_config.maximum_results_to_publish=InpMaximumConfirmationResults;
   config.lifecycle_config.confirmation_config.maximum_finalized_ids_to_remember=InpMaximumFinalizedIds;

   config.lifecycle_config.allow_repeat_across_new_opportunities_while_protected_survives=InpAllowRepeatAcrossNewOpportunitiesWhileProtectedSurvives;
   config.lifecycle_config.suppress_duplicate_exact_opportunity=InpSuppressDuplicateExactOpportunity;
   config.lifecycle_config.retire_on_protected_touch=InpRetireOnProtectedTouch; config.lifecycle_config.retire_on_double_hunt=InpRetireOnDoubleHunt;
   config.lifecycle_config.retire_on_role_switch=InpRetireOnRoleSwitch; config.lifecycle_config.preserve_accepted_uses_after_retirement=InpPreserveAcceptedUsesAfterRetirement;
   config.lifecycle_config.publish_rejected_uses=InpPublishRejectedUses; config.lifecycle_config.persist_checkpoint=InpPersistLifecycleCheckpoint;
   config.lifecycle_config.checkpoint_prefix=InpLifecycleCheckpointPrefix; config.lifecycle_config.maximum_reference_records=InpMaximumReferenceRecords;
   config.lifecycle_config.maximum_use_records=InpMaximumUseRecords; config.lifecycle_config.maximum_processed_result_ids=InpMaximumProcessedResultIds;

   config.target_policy=InpTargetChartPolicy; config.extreme_anchor_policy=InpReferenceExtremeAnchor;
   config.require_target_chart_host_timeframe=InpRequireTargetChartHostTimeframe;
   config.open_missing_hunter_chart=InpOpenMissingHunterChart; config.opened_chart_timeframe=InpOpenedChartTimeframe;
   config.line_color=InpDivergenceLineColor; config.line_style=InpDivergenceLineStyle; config.line_width=InpDivergenceLineWidth;
   config.line_ray_left=InpRayLeft; config.line_ray_right=InpRayRight; config.line_back=InpDrawInBackground;
   config.line_selectable=InpObjectsSelectable; config.line_hidden=InpObjectsHidden;
   config.show_major_labels=InpShowMajorSignalLabels; config.use_midpoint_text_object=InpUseMidpointTextObject;
   config.label_font=InpLabelFont; config.label_font_size=InpLabelFontSize; config.label_color=InpLabelColor;
   config.label_vertical_offset_points=InpLabelVerticalOffsetPoints;
   config.verify_existing_owned_objects=InpVerifyExistingOwnedObjects;
   config.repair_existing_owned_objects=InpRepairExistingOwnedObjects;
   config.recreate_manually_deleted_owned_objects=InpRecreateManuallyDeletedOwnedObjects;
   config.preserve_orphaned_owned_objects=InpPreserveOrphanedOwnedObjects;
   config.delete_owned_objects_on_deinit=InpDeleteOwnedObjectsOnDeinit;
   config.maximum_projection_records=InpMaximumProjectionRecords;
   config.maximum_target_charts_per_use=InpMaximumTargetChartsPerUse;
}

datetime DAYE_P08CurrentBrokerTime(void)
{
   datetime value=TimeTradeServer(); if(value<=0) value=TimeCurrent(); return value;
}

int OnInit()
{
   DAYE_TimeConfig time_config; DAYE_RenderConfig config;
   DAYE_BuildP08TimeConfig(time_config); DAYE_BuildP08Config(config);
   if(!g_daye_render_engine.Initialize(config,time_config,InpRunEmbeddedSelfTestsOnInit,InpWriteAuditCsv,InpAuditCsvFilename)) return INIT_FAILED;
   int timer_seconds=InpTimerSeconds; if(timer_seconds<1) timer_seconds=1;
   if(!EventSetTimer(timer_seconds)) { Print("EXP0018 P08 EventSetTimer failed error=",GetLastError()); g_daye_render_engine.Shutdown(); return INIT_FAILED; }
   datetime now=DAYE_P08CurrentBrokerTime();
   if(now>0) g_daye_render_engine.Process(now,InpPrintSummaryOnRefresh,InpPrintLatestProjection,InpPrintTransitionEvents,
                                          InpShowChartComment,InpWriteSummaryRows,InpAuditLatestProjectionCount);
   return INIT_SUCCEEDED;
}

void OnTimer()
{
   datetime now=DAYE_P08CurrentBrokerTime();
   if(now>0) g_daye_render_engine.Process(now,InpPrintSummaryOnRefresh,InpPrintLatestProjection,InpPrintTransitionEvents,
                                          InpShowChartComment,InpWriteSummaryRows,InpAuditLatestProjectionCount);
}

void OnTick()
{
   // Timer-driven immutable drawing projection only.
}

void OnDeinit(const int reason)
{
   EventKillTimer(); g_daye_render_engine.Shutdown();
}
