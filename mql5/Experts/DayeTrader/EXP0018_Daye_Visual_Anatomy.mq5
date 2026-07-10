#property strict
#property version   "2.11"
#property description "EXP0018 P10 unified Daye visual anatomy: divergence, cycles, boxes, micro quarters, TDO and TWO. No trading authority."

#include <DayeTrader/EXP0018/DAYE_VisualEngine.mqh>
#include <DayeTrader/EXP0018/DAYE_SymbolResolver.mqh>

input group "EXP0018 P08 — Symbols"
input string InpSymbolA="SPXUSD";
input string InpSymbolB="NDXUSD";
input string InpCanonicalSymbolA="SPX";
input string InpCanonicalSymbolB="NDX";

input group "EXP0018 P10 — Broker Symbol Recovery"
input bool InpAutoResolveBrokerSymbols=true;
input bool InpPreferCurrentChartSymbol=true;
input bool InpFailInitIfPairPipelineUnavailable=false;
input bool InpAllowSingleSymbolTimeFallback=true;
input int InpLocalVisualMinimumBars=60;
input bool InpPrintDetailedInitDiagnostics=true;

input group "EXP0018 P08 — Source and Host Timeframes"
input ENUM_TIMEFRAMES InpBaseTimeframe=PERIOD_M1;
input ENUM_TIMEFRAMES InpHostTimeframe=PERIOD_CURRENT;
input int InpRequestedBarsPerSymbol=30000;
input int InpMinimumCommonBars=500;
input int InpMaximumPairsToPublish=30000;
input int InpMinimumCompletePairedPeriods=10;
input int InpMaximumPeriodsToPublish=4000;
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


input group "EXP0018 P10 — Unified Visual Layers"
input bool InpRenderDailyFrame=true;
input bool InpRenderDailyBoundaries=true;
input bool InpRenderDailyLabel=true;
input bool InpRenderSessionBoxes=true;
input bool InpRenderSessionBoundaries=true;
input bool InpRenderSessionLabels=true;
input bool InpRenderSubcycleBoxes=true;
input bool InpRenderSubcycleBoundaries=true;
input bool InpRenderSubcycleLabels=true;
input bool InpRenderMicro225Boundaries=true;
input bool InpRenderMicro225Labels=true;
input bool InpRenderGapBand=true;
input bool InpRenderGapBoundaries=true;
input bool InpRenderTDO=true;
input bool InpRenderTWO=true;
input bool InpRenderExtendedSessionTrueOpens=false;
input bool InpRenderProvisionalWeekBoundaries=false;
input bool InpRenderVisualLegend=true;

input group "EXP0018 P10 — Visual Admission and Targeting"
input DAYE_VisualTargetPolicy InpVisualTargetPolicy=DAYE_VISUAL_TARGET_ALL_OPEN_SYMBOL_CHARTS;
input int InpVisualLookbackWeeks=2;
input int InpVisualMaximumTargetChartsPerSymbol=8;
input bool InpVisualOpenMissingSymbolChart=false;
input ENUM_TIMEFRAMES InpVisualOpenedChartTimeframe=PERIOD_M15;
input bool InpVisualRenderCompletePeriods=true;
input bool InpVisualRenderOpenPeriods=true;
input bool InpVisualRenderPartialPeriods=false;
input DAYE_TwoAnchorPolicy InpTwoAnchorPolicy=DAYE_TWO_TUESDAY_1800_LITERAL;
input DAYE_ProvisionalWeekPolicy InpProvisionalWeekPolicy=DAYE_WEEK_SUNDAY_1800_TO_FRIDAY_1700;

input group "EXP0018 P10 — Visual Colors"
input color InpDailyFrameColor=clrDimGray;
input color InpSessionAColor=clrSkyBlue;
input color InpSessionLColor=clrLime;
input color InpSessionNColor=clrOrange;
input color InpSessionPColor=C'255,128,128';
input color InpSubcycleColor=clrSlateGray;
input color InpMicro225Color=clrSilver;
input color InpGapColor=clrGray;
input color InpTDOColor=clrRed;
input color InpTWOColor=clrRed;
input color InpExtendedTrueOpenColor=clrDarkOrange;
input color InpProvisionalWeekColor=clrMediumPurple;
input color InpVisualLabelColor=clrGainsboro;

input group "EXP0018 P10 — Visual Style"
input int InpDailyFillAlpha=8;
input int InpSessionFillAlpha=35;
input int InpSubcycleFillAlpha=12;
input int InpGapFillAlpha=18;
input ENUM_LINE_STYLE InpMajorBoundaryStyle=STYLE_SOLID;
input ENUM_LINE_STYLE InpSubcycleBoundaryStyle=STYLE_DASH;
input ENUM_LINE_STYLE InpMicroBoundaryStyle=STYLE_DOT;
input int InpMajorBoundaryWidth=1;
input int InpSubcycleBoundaryWidth=1;
input int InpMicroBoundaryWidth=1;
input int InpOpenAnchorWidth=2;
input bool InpVisualBoxesInBackground=true;
input bool InpVisualObjectsSelectable=false;
input bool InpVisualObjectsHidden=false;
input string InpVisualLabelFont="Arial";
input int InpVisualMajorLabelFontSize=9;
input int InpVisualMinorLabelFontSize=8;
input double InpVisualLabelOffsetPoints=12.0;
input bool InpVisualVerifyObjects=true;
input bool InpVisualRepairObjects=true;
input bool InpVisualRecreateDeletedObjects=true;
input bool InpVisualDeleteObjectsOnDeinit=false;
input int InpVisualVerificationIntervalSeconds=10;

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


CDayeVisualEngine g_daye_visual_engine;
string g_daye_resolved_symbol_a="";
string g_daye_resolved_symbol_b="";
bool g_daye_pair_symbols_ready=false;

void DAYE_BuildP08TimeConfig(DAYE_TimeConfig &config)
{
   config.schema_version=DAYE_TIME_SCHEMA_VERSION;
   config.broker_offset_mode=InpBrokerOffsetMode;
   config.broker_utc_offset_minutes=(int)MathRound(InpBrokerUtcOffsetHours*60.0);
   config.ny_offset_mode=InpNewYorkOffsetMode;
   config.manual_new_york_utc_offset_minutes=(int)MathRound(InpManualNewYorkUtcOffsetHours*60.0);
   config.ambiguous_start_policy=InpAmbiguousStartPolicy;
   config.ambiguous_end_policy=InpAmbiguousEndPolicy;
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
   config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.broker_symbol_a=(g_daye_resolved_symbol_a!=""?g_daye_resolved_symbol_a:InpSymbolA); config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.broker_symbol_b=(g_daye_resolved_symbol_b!=""?g_daye_resolved_symbol_b:InpSymbolB);
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


void DAYE_BuildP10VisualConfig(DAYE_VisualConfig &config)
{
   ZeroMemory(config);
   config.schema_version=DAYE_VISUAL_SCHEMA_VERSION;
   config.target_policy=InpVisualTargetPolicy;
   config.lookback_weeks=InpVisualLookbackWeeks;
   config.maximum_target_charts_per_symbol=InpVisualMaximumTargetChartsPerSymbol;
   config.open_missing_symbol_chart=InpVisualOpenMissingSymbolChart;
   config.opened_chart_timeframe=InpVisualOpenedChartTimeframe;
   config.render_daily_frame=InpRenderDailyFrame;
   config.render_daily_boundaries=InpRenderDailyBoundaries;
   config.render_daily_label=InpRenderDailyLabel;
   config.render_session_boxes=InpRenderSessionBoxes;
   config.render_session_boundaries=InpRenderSessionBoundaries;
   config.render_session_labels=InpRenderSessionLabels;
   config.render_subcycle_boxes=InpRenderSubcycleBoxes;
   config.render_subcycle_boundaries=InpRenderSubcycleBoundaries;
   config.render_subcycle_labels=InpRenderSubcycleLabels;
   config.render_micro_22_5_boundaries=InpRenderMicro225Boundaries;
   config.render_micro_22_5_labels=InpRenderMicro225Labels;
   config.render_gap_band=InpRenderGapBand;
   config.render_gap_boundaries=InpRenderGapBoundaries;
   config.render_tdo=InpRenderTDO;
   config.render_two=InpRenderTWO;
   config.render_extended_session_true_opens=InpRenderExtendedSessionTrueOpens;
   config.render_provisional_week_boundaries=InpRenderProvisionalWeekBoundaries;
   config.render_legend=InpRenderVisualLegend;
   config.render_complete_periods=InpVisualRenderCompletePeriods;
   config.render_open_periods=InpVisualRenderOpenPeriods;
   config.render_partial_periods=InpVisualRenderPartialPeriods;
   config.two_anchor_policy=InpTwoAnchorPolicy;
   config.provisional_week_policy=InpProvisionalWeekPolicy;
   config.daily_color=InpDailyFrameColor;
   config.session_a_color=InpSessionAColor;
   config.session_l_color=InpSessionLColor;
   config.session_n_color=InpSessionNColor;
   config.session_p_color=InpSessionPColor;
   config.subcycle_color=InpSubcycleColor;
   config.micro_color=InpMicro225Color;
   config.gap_color=InpGapColor;
   config.tdo_color=InpTDOColor;
   config.two_color=InpTWOColor;
   config.true_open_color=InpExtendedTrueOpenColor;
   config.week_color=InpProvisionalWeekColor;
   config.label_color=InpVisualLabelColor;
   config.daily_fill_alpha=InpDailyFillAlpha;
   config.session_fill_alpha=InpSessionFillAlpha;
   config.subcycle_fill_alpha=InpSubcycleFillAlpha;
   config.gap_fill_alpha=InpGapFillAlpha;
   config.major_boundary_style=InpMajorBoundaryStyle;
   config.subcycle_boundary_style=InpSubcycleBoundaryStyle;
   config.micro_boundary_style=InpMicroBoundaryStyle;
   config.major_boundary_width=InpMajorBoundaryWidth;
   config.subcycle_boundary_width=InpSubcycleBoundaryWidth;
   config.micro_boundary_width=InpMicroBoundaryWidth;
   config.anchor_width=InpOpenAnchorWidth;
   config.draw_boxes_in_background=InpVisualBoxesInBackground;
   config.objects_selectable=InpVisualObjectsSelectable;
   config.objects_hidden=InpVisualObjectsHidden;
   config.label_font=InpVisualLabelFont;
   config.major_label_font_size=InpVisualMajorLabelFontSize;
   config.minor_label_font_size=InpVisualMinorLabelFontSize;
   config.label_vertical_offset_points=InpVisualLabelOffsetPoints;
   config.verify_existing_owned_objects=InpVisualVerifyObjects;
   config.repair_existing_owned_objects=InpVisualRepairObjects;
   config.recreate_manually_deleted_owned_objects=InpVisualRecreateDeletedObjects;
   config.delete_owned_objects_on_deinit=InpVisualDeleteObjectsOnDeinit;
   config.object_verification_interval_seconds=InpVisualVerificationIntervalSeconds;
   config.allow_single_symbol_time_fallback=InpAllowSingleSymbolTimeFallback;
   config.fail_init_when_pair_pipeline_unavailable=InpFailInitIfPairPipelineUnavailable;
   config.local_visual_minimum_bars=InpLocalVisualMinimumBars;
   config.print_detailed_source_diagnostics=InpPrintDetailedInitDiagnostics;
}

datetime DAYE_P10CurrentBrokerTime(void)
{
   datetime value=TimeTradeServer();
   if(value<=0) value=TimeCurrent();
   return value;
}

int OnInit()
{
   string resolution_report="";
   string current_chart_symbol=ChartSymbol(ChartID());
   g_daye_pair_symbols_ready=DAYE_ResolveBrokerPair(InpSymbolA,InpCanonicalSymbolA,
                                                    InpSymbolB,InpCanonicalSymbolB,
                                                    current_chart_symbol,
                                                    InpAutoResolveBrokerSymbols,
                                                    InpPreferCurrentChartSymbol,
                                                    g_daye_resolved_symbol_a,
                                                    g_daye_resolved_symbol_b,
                                                    resolution_report);
   Print("EXP0018 P10 symbol resolution: ",resolution_report,
         " | chart=",current_chart_symbol," tf=",EnumToString((ENUM_TIMEFRAMES)_Period));
   if(!g_daye_pair_symbols_ready && InpFailInitIfPairPipelineUnavailable)
   {
      Print("EXP0018 P10 initialization stopped: paired symbols unresolved and strict pair initialization is enabled.");
      return INIT_FAILED;
   }
   if(!g_daye_pair_symbols_ready)
      Print("EXP0018 P10 continuing in local time-anatomy mode. Divergence lines remain unavailable until both broker symbols resolve.");

   DAYE_TimeConfig time_config;
   DAYE_RenderConfig render_config;
   DAYE_VisualConfig visual_config;
   DAYE_BuildP08TimeConfig(time_config);
   DAYE_BuildP08Config(render_config);
   DAYE_BuildP10VisualConfig(visual_config);
   ResetLastError();
   if(!g_daye_visual_engine.Initialize(render_config,visual_config,time_config,
                                       InpRunEmbeddedSelfTestsOnInit,InpWriteAuditCsv,InpAuditCsvFilename))
   {
      Print("EXP0018 P10 initialization failed after symbol resolution. chart=",current_chart_symbol,
            " resolvedA=",g_daye_resolved_symbol_a," resolvedB=",g_daye_resolved_symbol_b,
            " last_error=",GetLastError());
      return INIT_FAILED;
   }
   int timer_seconds=InpTimerSeconds;
   if(timer_seconds<1) timer_seconds=1;
   ResetLastError();
   if(!EventSetTimer(timer_seconds))
   {
      Print("EXP0018 P10 EventSetTimer failed error=",GetLastError());
      g_daye_visual_engine.Shutdown();
      return INIT_FAILED;
   }
   datetime now=DAYE_P10CurrentBrokerTime();
   if(now>0)
   {
      if(!g_daye_visual_engine.Process(now,InpPrintSummaryOnRefresh,true,InpShowChartComment))
         Print("EXP0018 P10 first process call failed. The timer will retry.");
   }
   else
      Print("EXP0018 P10 current broker time unavailable during OnInit; timer will retry.");
   return INIT_SUCCEEDED;
}

void OnTimer()
{
   datetime now=DAYE_P10CurrentBrokerTime();
   if(now>0) g_daye_visual_engine.Process(now,InpPrintSummaryOnRefresh,true,InpShowChartComment);
}

void OnTick()
{
   // Timer-driven unified drawing projection only.
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_daye_visual_engine.Shutdown();
}
