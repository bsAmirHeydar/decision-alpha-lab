#property strict
#property version   "1.11"
#property description "EXP0017 Phase 14 - Modular raw execution backtest"
#property description "Closed-candle CG divergence entries with hard one-shot signal entitlement, modular targets, fixed-money risk, hedge control, and execution visuals."

#include <IntermarketDivergenceExecution/CG/Execution/CGX_Engine.mqh>

input group "EXP0017 / Signal Pair"
input string InpSymbolA = "SPXUSD";
input string InpSymbolB = "NDXUSD";

input group "EXP0017 / Time and Confirmation"
input int  InpBrokerUtcOffsetHours = 3;
input bool InpUseAutoNewYorkDst = true;
input int  InpManualNewYorkUtcOffsetHours = -5;
input ENUM_TIMEFRAMES InpConfirmationTimeframe = PERIOD_CURRENT;
input bool InpRequireM1History = true;

input group "EXP0017 / Reference Freshness and Lifecycle"
input bool InpEnableProtectedReferenceRetirement = true;
input bool InpRetireReferenceWhenProtectedHunts = true;
input bool InpAllowRepeatedDivergenceWhileProtectedSurvives = true;
input bool InpSuppressRetiredReferenceSignals = true;
input bool InpResetProtectedReferenceLifecycleAtNewTradingDay = true;
input int  InpMaxProtectedReferenceRecords = 4096;
input bool InpEnableExtremeFrontierReferenceFilter = true;
input bool InpRequireSymbolLocalFrontierForBothSymbols = true;
input bool InpSuppressNonFrontierReferenceSignals = true;

input group "EXP0017 / Execution Runtime"
input ECGXRuntimeMode InpRuntimeMode = CGX_RUNTIME_BACKTEST_ONLY;
input ECGXTradeLeg InpTradeLeg = CGX_TRADE_PROTECTED_SYMBOL;
input ECGXEntryModel InpEntryModel = CGX_ENTRY_MARKET_ON_CLOSED_CANDLE;
input bool InpProcessExistingClosedBarOnInit = false;

input group "EXP0017 / Stop Model"
input ECGXStopModel InpStopModel = CGX_STOP_BEHIND_CONFIRMATION_CANDLE;
input double InpStopBufferPoints = 0.0;
input bool InpAddSpreadToSellStop = true;

input group "EXP0017 / Target Model"
input ECGXTargetModel InpTargetModel = CGX_TARGET_ATR_MULTIPLE;
input int InpATRPeriod = 14;
input double InpATRMultiplier = 1.0;
input double InpRiskRewardMultiple = 1.0;

input group "EXP0017 / Volume and Risk"
input ECGXVolumeModel InpVolumeModel = CGX_VOLUME_FIXED_RISK_MONEY;
input double InpFixedRiskMoney = 100.0;
input double InpRiskPercentEquity = 1.0;
input double InpFixedLots = 0.10;
input bool InpAllowMinimumVolumeRiskOverflow = false;

input group "EXP0017 / Hedge and Position Policy"
input bool InpEnableHedging = true;
input bool InpRequireHedgingAccount = true;
input ECGXPositionPolicy InpPositionPolicy = CGX_POSITION_EVERY_SIGNAL;
input ECGXNettingPolicy InpNettingPolicy = CGX_NETTING_SKIP_WHEN_POSITION_EXISTS;

input group "EXP0017 / Broker Routing"
input long InpMagicBase = 17017000;
input int InpDeviationPoints = 30;
input double InpMaxSpreadPoints = 0.0;
input int InpMaxQuoteAgeSeconds = 0;

input group "EXP0017 / Execution Visuals"
input bool InpDrawExecutedCGSignals = true;
input bool InpDrawExecutionLevels = true;
input bool InpDrawOnBothInputSymbolCharts = true;
input bool InpOpenMissingVisualCharts = false;
input bool InpClearExecutionObjectsOnInit = true;
input bool InpClearExecutionObjectsOnDeinit = false;

input group "EXP0017 / Audit"
input bool InpPrintExecutionEvents = true;
input bool InpEnableExecutionAuditCsv = true;
input bool InpAuditUseCommonFiles = false;
input string InpAuditFileName = "EXP0017_Phase14_Raw_Execution_Audit_V3.csv";
input int InpMaxSignalRegistryRecords = 20000;

input group "EXP0017 / Enabled CG Trades"
input bool InpTrade_cg_3m   = true;
input bool InpTrade_cg_5m   = false;
input bool InpTrade_cg_9m   = false;
input bool InpTrade_cg_10m  = false;
input bool InpTrade_cg_15m  = false;
input bool InpTrade_cg_18m  = false;
input bool InpTrade_cg_20m  = false;
input bool InpTrade_cg_24m  = false;
input bool InpTrade_cg_30m  = false;
input bool InpTrade_cg_40m  = false;
input bool InpTrade_cg_45m  = false;
input bool InpTrade_cg_60m  = false;
input bool InpTrade_cg_72m  = false;
input bool InpTrade_cg_90m  = false;
input bool InpTrade_cg_120m = false;
input bool InpTrade_cg_150m = false;
input bool InpTrade_cg_180m = false;
input bool InpTrade_cg_240m = false;
input bool InpTrade_cg_300m = false;
input bool InpTrade_cg_360m = false;
input bool InpTrade_cg_720m = false;

CCGX_Engine g_engine;

void LoadEnabledGroups(bool &enabled[])
{
   ArrayResize(enabled,CGT_GROUP_COUNT);
   enabled[CGT_CG3M]=InpTrade_cg_3m;
   enabled[CGT_CG5M]=InpTrade_cg_5m;
   enabled[CGT_CG9M]=InpTrade_cg_9m;
   enabled[CGT_CG10M]=InpTrade_cg_10m;
   enabled[CGT_CG15M]=InpTrade_cg_15m;
   enabled[CGT_CG18M]=InpTrade_cg_18m;
   enabled[CGT_CG20M]=InpTrade_cg_20m;
   enabled[CGT_CG24M]=InpTrade_cg_24m;
   enabled[CGT_CG30M]=InpTrade_cg_30m;
   enabled[CGT_CG40M]=InpTrade_cg_40m;
   enabled[CGT_CG45M]=InpTrade_cg_45m;
   enabled[CGT_CG60M]=InpTrade_cg_60m;
   enabled[CGT_CG72M]=InpTrade_cg_72m;
   enabled[CGT_CG90M]=InpTrade_cg_90m;
   enabled[CGT_CG120M]=InpTrade_cg_120m;
   enabled[CGT_CG150M]=InpTrade_cg_150m;
   enabled[CGT_CG180M]=InpTrade_cg_180m;
   enabled[CGT_CG240M]=InpTrade_cg_240m;
   enabled[CGT_CG300M]=InpTrade_cg_300m;
   enabled[CGT_CG360M]=InpTrade_cg_360m;
   enabled[CGT_CG720M]=InpTrade_cg_720m;
}

void LoadTimeConfig(SCGTTimeConfig &config)
{
   config.broker_utc_offset_hours=InpBrokerUtcOffsetHours;
   config.use_auto_new_york_dst=InpUseAutoNewYorkDst;
   config.manual_new_york_utc_offset_hours=InpManualNewYorkUtcOffsetHours;
   config.max_previous_cycles_shown=0;
}

void LoadConfirmationConfig(SCGCConfirmationConfig &config)
{
   config.symbol_a=InpSymbolA;
   config.symbol_b=InpSymbolB;
   config.broker_utc_offset_hours=InpBrokerUtcOffsetHours;
   config.confirmation_timeframe=InpConfirmationTimeframe;
   config.use_last_closed_candle_boundary=true;
   config.max_groups_shown=CGT_GROUP_COUNT;
   config.max_signals_per_group_shown=0;
   config.require_m1_history=InpRequireM1History;
   config.show_only_groups_with_final_states=false;
   config.show_invalidated_double_hunts=false;
   config.show_prices=false;
   config.show_stop_reference_preview=false;
   config.enable_protected_reference_retirement=InpEnableProtectedReferenceRetirement;
   config.retire_reference_when_protected_hunts=InpRetireReferenceWhenProtectedHunts;
   config.allow_repeated_divergence_while_protected_survives=InpAllowRepeatedDivergenceWhileProtectedSurvives;
   config.suppress_retired_reference_signals=InpSuppressRetiredReferenceSignals;
   config.reset_lifecycle_at_new_trading_day=InpResetProtectedReferenceLifecycleAtNewTradingDay;
   config.max_protected_reference_records=InpMaxProtectedReferenceRecords;
   config.enable_extreme_frontier_reference_filter=InpEnableExtremeFrontierReferenceFilter;
   config.require_symbol_local_frontier_for_both_symbols=InpRequireSymbolLocalFrontierForBothSymbols;
   config.suppress_non_frontier_reference_signals=InpSuppressNonFrontierReferenceSignals;
}

void LoadExecutionConfig(SCGXExecutionConfig &config)
{
   config.runtime_mode=InpRuntimeMode;
   config.trade_leg=InpTradeLeg;
   config.entry_model=InpEntryModel;
   config.stop_model=InpStopModel;
   config.target_model=InpTargetModel;
   config.volume_model=InpVolumeModel;
   config.position_policy=InpPositionPolicy;
   config.netting_policy=InpNettingPolicy;
   config.enable_hedging=InpEnableHedging;
   config.require_hedging_account=InpRequireHedgingAccount;
   config.stop_buffer_points=InpStopBufferPoints;
   config.add_spread_to_sell_stop=InpAddSpreadToSellStop;
   config.atr_period=InpATRPeriod;
   config.atr_multiplier=InpATRMultiplier;
   config.risk_reward_multiple=InpRiskRewardMultiple;
   config.fixed_risk_money=InpFixedRiskMoney;
   config.risk_percent_equity=InpRiskPercentEquity;
   config.fixed_lots=InpFixedLots;
   config.allow_minimum_volume_risk_overflow=InpAllowMinimumVolumeRiskOverflow;
   config.magic_base=InpMagicBase;
   config.deviation_points=InpDeviationPoints;
   config.max_spread_points=InpMaxSpreadPoints;
   config.max_quote_age_seconds=InpMaxQuoteAgeSeconds;
   config.process_existing_closed_bar_on_init=InpProcessExistingClosedBarOnInit;
   config.print_execution_events=InpPrintExecutionEvents;
   config.enable_audit_csv=InpEnableExecutionAuditCsv;
   config.audit_use_common_files=InpAuditUseCommonFiles;
   config.audit_file_name=InpAuditFileName;
   config.max_signal_registry_records=InpMaxSignalRegistryRecords;
   config.draw_executed_signals=InpDrawExecutedCGSignals;
   config.draw_execution_levels=InpDrawExecutionLevels;
   config.draw_on_both_input_symbol_charts=InpDrawOnBothInputSymbolCharts;
   config.open_missing_visual_charts=InpOpenMissingVisualCharts;
   config.clear_execution_objects_on_init=InpClearExecutionObjectsOnInit;
   config.clear_execution_objects_on_deinit=InpClearExecutionObjectsOnDeinit;
   config.symbol_a=InpSymbolA;
   config.symbol_b=InpSymbolB;
}

int OnInit()
{
   if(InpSymbolA=="" || InpSymbolB=="" || InpSymbolA==InpSymbolB)
   {
      Print("EXP0017 Phase14 init failed: two distinct non-empty symbols are required.");
      return INIT_PARAMETERS_INCORRECT;
   }
   if(!SymbolSelect(InpSymbolA,true) || !SymbolSelect(InpSymbolB,true))
   {
      Print("EXP0017 Phase14 init failed: symbol selection failed.");
      return INIT_FAILED;
   }

   SCGTTimeConfig time_config;
   SCGCConfirmationConfig confirmation_config;
   SCGXExecutionConfig execution_config;
   bool enabled[];
   LoadTimeConfig(time_config);
   LoadConfirmationConfig(confirmation_config);
   LoadExecutionConfig(execution_config);
   LoadEnabledGroups(enabled);

   if(!g_engine.Init(time_config,confirmation_config,execution_config,enabled))
      return INIT_PARAMETERS_INCORRECT;
   return INIT_SUCCEEDED;
}

void OnTick()
{
   g_engine.Pulse();
}

void OnDeinit(const int reason)
{
   g_engine.Clear();
}
