#property strict
#property version   "1.00"
#property description "EXP0017 Phase 07 - Signal Outcome Study Anatomy"
#property description "No trading. Studies confirmed EXP0017 signals and writes outcome metrics to CSV."

#include <IntermarketDivergenceExecution/CG/CGO_Engine.mqh>

input string InpSymbolA = "SPXUSD";
input string InpSymbolB = "NDXUSD";

input int  InpBrokerUtcOffsetHours = 3;
input bool InpUseAutoNewYorkDst = true;
input int  InpManualNewYorkUtcOffsetHours = -5;

input ENUM_TIMEFRAMES InpConfirmationTimeframe = PERIOD_CURRENT;
input bool InpUseLastClosedCandleBoundary = true;
input bool InpRequireM1History = true;

// Phase 07 historical outcome study. This phase studies past confirmed signals only.
input bool InpRunHistoricalOutcomeStudyOnInit = true;
input int  InpHistoricalLookbackTradingDays = 5;
input int  InpHistoricalMaxClosedCandles = 1200;
input int  InpMaxOutcomeRowsToWrite = 5000;
input bool InpPrintStudySummary = true;
input bool InpShowChartPanel = false;
input int  InpTimerSeconds = 10;
input bool InpProcessLatestClosedCandleOnTimer = false;

// Entry/exit model for study only. No order is sent.
input ECGOEntryPriceMode InpEntryPriceMode = CGO_ENTRY_CONFIRMATION_CLOSE;
input ENUM_TIMEFRAMES InpOutcomeExecutionTimeframe = PERIOD_M1;
input bool InpRequireCompleteFutureWindow = true;
input bool InpSkipSignalsWithZeroRisk = true;
input double InpMinimumRiskPoints = 0.1;
input int InpStudyForwardCycles = 3;
input bool InpStudyCycleEndOutcome = true;
input bool InpStudyForwardCycleWindows = true;
input bool InpStudyDayEndOutcome = true;
input bool InpStudyMaxIntradayReward = true;
input bool InpDetectStopBeforeWindowClose = true;
input bool InpUseCleanSymbolDailyRangeForNormalization = true;

// CSV ledger.
input bool InpEnableOutcomeLedger = true;
input bool InpLedgerUseCommonFiles = false;
input string InpOutcomeLedgerFileName = "EXP0017_Phase07_Outcome_Study.csv";
input bool InpClearOutcomeLedgerOnInit = true;
input bool InpUseInMemoryDuplicateGuard = true;

// Keep current Phase 05/06 reference integrity rules active.
input bool InpEnableProtectedReferenceRetirement = true;
input bool InpRetireReferenceWhenProtectedHunts = true;
input bool InpAllowRepeatedDivergenceWhileProtectedSurvives = true;
input bool InpSuppressRetiredReferenceSignals = true;
input bool InpResetProtectedReferenceLifecycleAtNewTradingDay = true;
input int  InpMaxProtectedReferenceRecords = 4096;
input bool InpEnableExtremeFrontierReferenceFilter = true;
input bool InpRequireSymbolLocalFrontierForBothSymbols = true;
input bool InpSuppressNonFrontierReferenceSignals = true;

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

CCGO_Engine g_engine;

int OnInit()
{
   SymbolSelect(InpSymbolA,true);
   SymbolSelect(InpSymbolB,true);

   SCGTTimeConfig time_config;
   time_config.broker_utc_offset_hours=InpBrokerUtcOffsetHours;
   time_config.use_auto_new_york_dst=InpUseAutoNewYorkDst;
   time_config.manual_new_york_utc_offset_hours=InpManualNewYorkUtcOffsetHours;
   time_config.max_previous_cycles_shown=0;

   SCGCConfirmationConfig confirmation_config;
   confirmation_config.symbol_a=InpSymbolA;
   confirmation_config.symbol_b=InpSymbolB;
   confirmation_config.broker_utc_offset_hours=InpBrokerUtcOffsetHours;
   confirmation_config.confirmation_timeframe=InpConfirmationTimeframe;
   confirmation_config.use_last_closed_candle_boundary=InpUseLastClosedCandleBoundary;
   confirmation_config.max_groups_shown=21;
   confirmation_config.max_signals_per_group_shown=1000;
   confirmation_config.require_m1_history=InpRequireM1History;
   confirmation_config.show_only_groups_with_final_states=false;
   confirmation_config.show_invalidated_double_hunts=false;
   confirmation_config.show_prices=true;
   confirmation_config.show_stop_reference_preview=true;
   confirmation_config.enable_protected_reference_retirement=InpEnableProtectedReferenceRetirement;
   confirmation_config.retire_reference_when_protected_hunts=InpRetireReferenceWhenProtectedHunts;
   confirmation_config.allow_repeated_divergence_while_protected_survives=InpAllowRepeatedDivergenceWhileProtectedSurvives;
   confirmation_config.suppress_retired_reference_signals=InpSuppressRetiredReferenceSignals;
   confirmation_config.reset_lifecycle_at_new_trading_day=InpResetProtectedReferenceLifecycleAtNewTradingDay;
   confirmation_config.max_protected_reference_records=InpMaxProtectedReferenceRecords;
   confirmation_config.enable_extreme_frontier_reference_filter=InpEnableExtremeFrontierReferenceFilter;
   confirmation_config.require_symbol_local_frontier_for_both_symbols=InpRequireSymbolLocalFrontierForBothSymbols;
   confirmation_config.suppress_non_frontier_reference_signals=InpSuppressNonFrontierReferenceSignals;

   SCGOOutcomeConfig outcome_config;
   outcome_config.symbol_a=InpSymbolA;
   outcome_config.symbol_b=InpSymbolB;
   outcome_config.entry_price_mode=InpEntryPriceMode;
   outcome_config.execution_timeframe=InpOutcomeExecutionTimeframe;
   outcome_config.require_complete_future_window=InpRequireCompleteFutureWindow;
   outcome_config.skip_zero_risk=InpSkipSignalsWithZeroRisk;
   outcome_config.minimum_risk_points=InpMinimumRiskPoints;
   outcome_config.forward_cycles=InpStudyForwardCycles;
   outcome_config.study_cycle_end=InpStudyCycleEndOutcome;
   outcome_config.study_forward_cycles=InpStudyForwardCycleWindows;
   outcome_config.study_day_end=InpStudyDayEndOutcome;
   outcome_config.study_intraday_extremes=InpStudyMaxIntradayReward;
   outcome_config.detect_stop_before_window_close=InpDetectStopBeforeWindowClose;
   outcome_config.use_clean_symbol_daily_range_for_normalization=InpUseCleanSymbolDailyRangeForNormalization;
   outcome_config.enable_ledger=InpEnableOutcomeLedger;
   outcome_config.ledger_use_common_files=InpLedgerUseCommonFiles;
   outcome_config.ledger_file_name=InpOutcomeLedgerFileName;
   outcome_config.clear_ledger_on_init=InpClearOutcomeLedgerOnInit;
   outcome_config.use_in_memory_duplicate_guard=InpUseInMemoryDuplicateGuard;
   outcome_config.max_rows_to_write=InpMaxOutcomeRowsToWrite;
   outcome_config.show_chart_panel=InpShowChartPanel;
   outcome_config.print_summary=InpPrintStudySummary;

   bool enabled[CGT_GROUP_COUNT];
   enabled[CGT_CG3M]=InpBuild_cg_3m;
   enabled[CGT_CG5M]=InpBuild_cg_5m;
   enabled[CGT_CG9M]=InpBuild_cg_9m;
   enabled[CGT_CG10M]=InpBuild_cg_10m;
   enabled[CGT_CG15M]=InpBuild_cg_15m;
   enabled[CGT_CG18M]=InpBuild_cg_18m;
   enabled[CGT_CG20M]=InpBuild_cg_20m;
   enabled[CGT_CG24M]=InpBuild_cg_24m;
   enabled[CGT_CG30M]=InpBuild_cg_30m;
   enabled[CGT_CG40M]=InpBuild_cg_40m;
   enabled[CGT_CG45M]=InpBuild_cg_45m;
   enabled[CGT_CG60M]=InpBuild_cg_60m;
   enabled[CGT_CG72M]=InpBuild_cg_72m;
   enabled[CGT_CG90M]=InpBuild_cg_90m;
   enabled[CGT_CG120M]=InpBuild_cg_120m;
   enabled[CGT_CG150M]=InpBuild_cg_150m;
   enabled[CGT_CG180M]=InpBuild_cg_180m;
   enabled[CGT_CG240M]=InpBuild_cg_240m;
   enabled[CGT_CG300M]=InpBuild_cg_300m;
   enabled[CGT_CG360M]=InpBuild_cg_360m;
   enabled[CGT_CG720M]=InpBuild_cg_720m;

   g_engine.Init(time_config,confirmation_config,outcome_config,enabled);

   if(InpRunHistoricalOutcomeStudyOnInit)
      g_engine.RunHistoricalStudy(InpHistoricalLookbackTradingDays,InpHistoricalMaxClosedCandles);

   EventSetTimer(InpTimerSeconds);
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_engine.Clear();
}

void OnTimer()
{
   if(InpProcessLatestClosedCandleOnTimer)
      g_engine.ProcessLatestClosedCandle();
}

void OnTick()
{
}
