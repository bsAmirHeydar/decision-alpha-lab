#property strict
#property version   "1.11"
#property description "EXP0017 Phase 06 - Cycle Group Visual Language and Signal Audit Ledger"
#property description "No trading. Hotfix011 proves SPX and NDX reference freshness independently from each symbol raw M1 path and renders stored local anchors."

#include <IntermarketDivergenceExecution/CG/CGV_Engine.mqh>

input string InpSymbolA = "SPXUSD";
input string InpSymbolB = "NDXUSD";

input int  InpBrokerUtcOffsetHours = 3;
input bool InpUseAutoNewYorkDst = true;
input int  InpManualNewYorkUtcOffsetHours = -5;

input ENUM_TIMEFRAMES InpConfirmationTimeframe = PERIOD_CURRENT;
input bool InpUseLastClosedCandleBoundary = true;
input bool InpShowChartPanel = false;
input bool InpPrintSummaryOnNewClosedCandle = false;

// Hotfix005 — historical visual backfill. Draw prior confirmed/invalidated states when the EA is attached.
input bool InpEnableHistoricalVisualBackfill = true;
input int  InpHistoricalBackfillLookbackTradingDays = 2;
input int  InpHistoricalBackfillMaxClosedCandles = 350;
input int  InpMaxHistoricalVisualDraws = 250;
input bool InpHistoricalBackfillWriteLedger = false;
input bool InpHistoricalBackfillPrintSummary = true;
input bool InpKeepFirstVisualForSameSignalId = true;
input int  InpTimerSeconds = 5;
input int  InpMaxGroupsShown = 8;
input int  InpMaxSignalsPerGroupShown = 6;
input bool InpRequireM1History = true;
input bool InpShowOnlyGroupsWithFinalStates = false;
input bool InpShowInvalidatedDoubleHunts = true;
input bool InpShowPrices = true;
input bool InpShowStopReferencePreview = true;

// Hotfix007 — protected-reference lifecycle. A same reference side may repeat only while the protected symbol stays protected.
input bool InpEnableProtectedReferenceRetirement = true;
input bool InpRetireReferenceWhenProtectedHunts = true;
input bool InpAllowRepeatedDivergenceWhileProtectedSurvives = true;
input bool InpSuppressRetiredReferenceSignals = true;
input bool InpResetProtectedReferenceLifecycleAtNewTradingDay = true;
input int  InpMaxProtectedReferenceRecords = 4096;

// Hotfix008 — only compare against unbroken extreme-frontier references.
input bool InpEnableExtremeFrontierReferenceFilter = true;
input bool InpRequireSymbolLocalFrontierForBothSymbols = true;
input bool InpSuppressNonFrontierReferenceSignals = true;

input bool InpEnableDrawing = true;
input ECGVVisualMode InpVisualMode = CGV_VISUAL_MODE_MINIMAL_LINES_ONLY;
input bool InpSuppressAllTextObjects = true;
input bool InpDeleteTextObjectsWhenSuppressed = true;
input bool InpForceAllVisualObjectsOn = false;
input bool InpClearPhase06ObjectsOnInit = true;
input bool InpClearPhase06ObjectsOnDeinit = false;
input bool InpDrawOnlyWhenChartIsHunterSymbol = false;
input bool InpDrawOnBothInputSymbolCharts = true;
input bool InpOpenMissingInputSymbolCharts = true;
input ENUM_TIMEFRAMES InpVisualChartTimeframe = PERIOD_CURRENT;
input bool InpDrawConfirmedTradeable = true;
input bool InpDrawInvalidatedDoubleHunts = false;
input bool InpDrawReferenceCycleAnchor = false;
input bool InpDrawConfirmationMarker = false;
input bool InpDrawTextLabel = false;
input int  InpLineWidth = 2;
input color InpBuyColor = clrLime;
input color InpSellColor = clrTomato;
input color InpInvalidatedColor = clrSilver;
input color InpTextColor = clrWhite;

// Hotfix002 — full origin-to-destination divergence visual language.
input bool InpDrawDivergenceOriginDestinationLine = true;
input ECGVAnchorSymbolMode InpDivergenceOriginSymbolMode = CGV_ANCHOR_SYMBOL_HUNTER;
input ECGVAnchorTimeMode   InpDivergenceOriginTimeMode = CGV_ANCHOR_TIME_EXACT_REFERENCE_EXTREME;
input ECGVAnchorPriceMode  InpDivergenceOriginPriceMode = CGV_ANCHOR_PRICE_HUNTER_REFERENCE;
input ECGVAnchorSymbolMode InpDivergenceDestinationSymbolMode = CGV_ANCHOR_SYMBOL_HUNTER;
input ECGVAnchorTimeMode   InpDivergenceDestinationTimeMode = CGV_ANCHOR_TIME_EXACT_CURRENT_EXTREME;
input ECGVAnchorPriceMode  InpDivergenceDestinationPriceMode = CGV_ANCHOR_PRICE_HUNTER_CURRENT_EXTREME;
input ECGVVisualLineStyle  InpDivergenceLineStyle = CGV_VISUAL_STYLE_SOLID;
input int  InpDivergenceLineWidth = 2;
input bool InpDrawOriginMarker = false;
input bool InpDrawDestinationMarker = false;
input int  InpOriginMarkerArrowCode = 159;
input int  InpDestinationMarkerArrowCode = 159;
input int  InpOriginMarkerWidth = 2;
input int  InpDestinationMarkerWidth = 2;
input bool InpDrawOriginVertical = false;
input bool InpDrawDestinationVertical = false;
input bool InpDrawHunterReferenceGuide = false;
input bool InpDrawCleanReferenceGuide = false;
input bool InpDrawCleanStopReferenceGuide = false;
input bool InpDrawHunterCurrentExtremeGuide = false;
input bool InpDrawCleanComparisonLine = false;
input bool InpDrawCleanComparisonOnlyWhenChartIsCleanSymbol = true;
input ECGVVisualLineStyle InpGuideLineStyle = CGV_VISUAL_STYLE_DOT;
input int  InpGuideLineWidth = 1;
input int  InpLabelFontSize = 8;
input double InpLabelOffsetPoints = 20.0;
input color InpOriginMarkerColor = clrDeepSkyBlue;
input color InpDestinationMarkerColor = clrGold;
input color InpGuideColor = clrSlateGray;
input color InpCleanComparisonColor = clrDodgerBlue;

input bool InpEnableLedger = true;
input bool InpLedgerUseCommonFiles = false;
input string InpLedgerFileName = "EXP0017_Phase06_Signal_Audit_Ledger.csv";
input bool InpWriteConfirmedToLedger = true;
input bool InpWriteInvalidatedToLedger = true;
input bool InpUseFileDuplicateGuard = true;

input bool InpBuild_cg_3m   = true;
input bool InpBuild_cg_5m   = true;
input bool InpBuild_cg_9m   = true;
input bool InpBuild_cg_10m  = true;
input bool InpBuild_cg_15m  = true;
input bool InpBuild_cg_18m  = true;
input bool InpBuild_cg_20m  = true;
input bool InpBuild_cg_24m  = true;
input bool InpBuild_cg_30m  = true;
input bool InpBuild_cg_40m  = true;
input bool InpBuild_cg_45m  = true;
input bool InpBuild_cg_60m  = true;
input bool InpBuild_cg_72m  = true;
input bool InpBuild_cg_90m  = true;
input bool InpBuild_cg_120m = true;
input bool InpBuild_cg_150m = true;
input bool InpBuild_cg_180m = true;
input bool InpBuild_cg_240m = true;
input bool InpBuild_cg_300m = true;
input bool InpBuild_cg_360m = true;
input bool InpBuild_cg_720m = true;

CCGV_Engine g_engine;

int OnInit()
{
   SymbolSelect(InpSymbolA,true);
   SymbolSelect(InpSymbolB,true);

   SCGTTimeConfig time_config;
   time_config.broker_utc_offset_hours=InpBrokerUtcOffsetHours;
   time_config.use_auto_new_york_dst=InpUseAutoNewYorkDst;
   time_config.manual_new_york_utc_offset_hours=InpManualNewYorkUtcOffsetHours;
   time_config.max_previous_cycles_shown=InpMaxSignalsPerGroupShown;

   SCGVVisualLedgerConfig config;
   config.symbol_a=InpSymbolA;
   config.symbol_b=InpSymbolB;
   config.broker_utc_offset_hours=InpBrokerUtcOffsetHours;
   config.confirmation_timeframe=InpConfirmationTimeframe;
   config.use_last_closed_candle_boundary=InpUseLastClosedCandleBoundary;
   config.max_groups_shown=InpMaxGroupsShown;
   config.max_signals_per_group_shown=InpMaxSignalsPerGroupShown;
   config.require_m1_history=InpRequireM1History;
   config.show_only_groups_with_final_states=InpShowOnlyGroupsWithFinalStates;
   config.show_invalidated_double_hunts=InpShowInvalidatedDoubleHunts;
   config.show_prices=InpShowPrices;
   config.show_stop_reference_preview=InpShowStopReferencePreview;
   config.enable_protected_reference_retirement=InpEnableProtectedReferenceRetirement;
   config.retire_reference_when_protected_hunts=InpRetireReferenceWhenProtectedHunts;
   config.allow_repeated_divergence_while_protected_survives=InpAllowRepeatedDivergenceWhileProtectedSurvives;
   config.suppress_retired_reference_signals=InpSuppressRetiredReferenceSignals;
   config.reset_lifecycle_at_new_trading_day=InpResetProtectedReferenceLifecycleAtNewTradingDay;
   config.max_protected_reference_records=InpMaxProtectedReferenceRecords;
   config.enable_extreme_frontier_reference_filter=InpEnableExtremeFrontierReferenceFilter;
   config.require_symbol_local_frontier_for_both_symbols=InpRequireSymbolLocalFrontierForBothSymbols;
   config.suppress_non_frontier_reference_signals=InpSuppressNonFrontierReferenceSignals;
   config.enable_drawing=InpEnableDrawing;
   config.visual_mode=InpVisualMode;
   config.suppress_all_text_objects=InpSuppressAllTextObjects;
   config.delete_text_objects_when_suppressed=InpDeleteTextObjectsWhenSuppressed;
   config.force_all_visual_objects_on=InpForceAllVisualObjectsOn;
   config.clear_objects_on_init=InpClearPhase06ObjectsOnInit;
   config.clear_objects_on_deinit=InpClearPhase06ObjectsOnDeinit;
   config.draw_only_when_chart_is_hunter_symbol=InpDrawOnlyWhenChartIsHunterSymbol;
   config.draw_on_both_input_symbol_charts=InpDrawOnBothInputSymbolCharts;
   config.open_missing_input_symbol_charts=InpOpenMissingInputSymbolCharts;
   config.visual_chart_timeframe=InpVisualChartTimeframe;
   config.draw_confirmed_tradeable=InpDrawConfirmedTradeable;
   config.draw_invalidated_double_hunts=InpDrawInvalidatedDoubleHunts;
   config.draw_reference_cycle_anchor=InpDrawReferenceCycleAnchor;
   config.draw_confirmation_marker=InpDrawConfirmationMarker;
   config.draw_text_label=InpDrawTextLabel;
   config.line_width=InpLineWidth;
   config.buy_color=InpBuyColor;
   config.sell_color=InpSellColor;
   config.invalidated_color=InpInvalidatedColor;
   config.text_color=InpTextColor;

   config.draw_divergence_origin_destination_line=InpDrawDivergenceOriginDestinationLine;
   config.divergence_origin_symbol_mode=InpDivergenceOriginSymbolMode;
   config.divergence_origin_time_mode=InpDivergenceOriginTimeMode;
   config.divergence_origin_price_mode=InpDivergenceOriginPriceMode;
   config.divergence_destination_symbol_mode=InpDivergenceDestinationSymbolMode;
   config.divergence_destination_time_mode=InpDivergenceDestinationTimeMode;
   config.divergence_destination_price_mode=InpDivergenceDestinationPriceMode;
   config.divergence_line_style=InpDivergenceLineStyle;
   config.divergence_line_width=InpDivergenceLineWidth;
   config.draw_origin_marker=InpDrawOriginMarker;
   config.draw_destination_marker=InpDrawDestinationMarker;
   config.origin_marker_arrow_code=InpOriginMarkerArrowCode;
   config.destination_marker_arrow_code=InpDestinationMarkerArrowCode;
   config.origin_marker_width=InpOriginMarkerWidth;
   config.destination_marker_width=InpDestinationMarkerWidth;
   config.draw_origin_vertical=InpDrawOriginVertical;
   config.draw_destination_vertical=InpDrawDestinationVertical;
   config.draw_hunter_reference_guide=InpDrawHunterReferenceGuide;
   config.draw_clean_reference_guide=InpDrawCleanReferenceGuide;
   config.draw_clean_stop_reference_guide=InpDrawCleanStopReferenceGuide;
   config.draw_hunter_current_extreme_guide=InpDrawHunterCurrentExtremeGuide;
   config.draw_clean_comparison_line=InpDrawCleanComparisonLine;
   config.draw_clean_comparison_only_when_chart_is_clean_symbol=InpDrawCleanComparisonOnlyWhenChartIsCleanSymbol;
   config.guide_line_style=InpGuideLineStyle;
   config.guide_line_width=InpGuideLineWidth;
   config.label_font_size=InpLabelFontSize;
   config.label_offset_points=InpLabelOffsetPoints;
   config.origin_marker_color=InpOriginMarkerColor;
   config.destination_marker_color=InpDestinationMarkerColor;
   config.guide_color=InpGuideColor;
   config.clean_comparison_color=InpCleanComparisonColor;
   config.max_historical_visual_draws=InpMaxHistoricalVisualDraws;

   config.enable_ledger=InpEnableLedger;
   config.ledger_use_common_files=InpLedgerUseCommonFiles;
   config.ledger_file_name=InpLedgerFileName;
   config.write_confirmed_to_ledger=InpWriteConfirmedToLedger;
   config.write_invalidated_to_ledger=InpWriteInvalidatedToLedger;
   config.use_file_duplicate_guard=InpUseFileDuplicateGuard;

   config.enable_historical_visual_backfill=InpEnableHistoricalVisualBackfill;
   config.historical_backfill_lookback_trading_days=InpHistoricalBackfillLookbackTradingDays;
   config.historical_backfill_max_closed_candles=InpHistoricalBackfillMaxClosedCandles;
   config.historical_backfill_write_ledger=InpHistoricalBackfillWriteLedger;
   config.historical_backfill_print_summary=InpHistoricalBackfillPrintSummary;
   config.keep_first_visual_for_same_signal_id=InpKeepFirstVisualForSameSignalId;

   bool enabled[CGT_GROUP_COUNT];
   enabled[CGT_CG3M]   = InpBuild_cg_3m;
   enabled[CGT_CG5M]   = InpBuild_cg_5m;
   enabled[CGT_CG9M]   = InpBuild_cg_9m;
   enabled[CGT_CG10M]  = InpBuild_cg_10m;
   enabled[CGT_CG15M]  = InpBuild_cg_15m;
   enabled[CGT_CG18M]  = InpBuild_cg_18m;
   enabled[CGT_CG20M]  = InpBuild_cg_20m;
   enabled[CGT_CG24M]  = InpBuild_cg_24m;
   enabled[CGT_CG30M]  = InpBuild_cg_30m;
   enabled[CGT_CG40M]  = InpBuild_cg_40m;
   enabled[CGT_CG45M]  = InpBuild_cg_45m;
   enabled[CGT_CG60M]  = InpBuild_cg_60m;
   enabled[CGT_CG72M]  = InpBuild_cg_72m;
   enabled[CGT_CG90M]  = InpBuild_cg_90m;
   enabled[CGT_CG120M] = InpBuild_cg_120m;
   enabled[CGT_CG150M] = InpBuild_cg_150m;
   enabled[CGT_CG180M] = InpBuild_cg_180m;
   enabled[CGT_CG240M] = InpBuild_cg_240m;
   enabled[CGT_CG300M] = InpBuild_cg_300m;
   enabled[CGT_CG360M] = InpBuild_cg_360m;
   enabled[CGT_CG720M] = InpBuild_cg_720m;

   g_engine.Init(time_config,config,enabled,InpShowChartPanel,InpPrintSummaryOnNewClosedCandle);
   EventSetTimer(MathMax(1,InpTimerSeconds));
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_engine.Clear();
}

void OnTick()
{
   g_engine.Pulse();
}

void OnTimer()
{
   g_engine.Pulse();
}
