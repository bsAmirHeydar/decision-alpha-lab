#property strict
#property version   "1.00"
#property description "EXP0017 Phase 06 - Cycle Group Visual Language and Signal Audit Ledger"
#property description "No trading. Draws confirmed/invalidated closed-candle states and records a raw CSV audit ledger."

#include <IntermarketDivergenceExecution/CG/CGV_Engine.mqh>

input string InpSymbolA = "SPXUSD";
input string InpSymbolB = "NDXUSD";

input int  InpBrokerUtcOffsetHours = 3;
input bool InpUseAutoNewYorkDst = true;
input int  InpManualNewYorkUtcOffsetHours = -5;

input ENUM_TIMEFRAMES InpConfirmationTimeframe = PERIOD_CURRENT;
input bool InpUseLastClosedCandleBoundary = true;
input bool InpShowChartPanel = true;
input bool InpPrintSummaryOnNewClosedCandle = false;
input int  InpTimerSeconds = 5;
input int  InpMaxGroupsShown = 8;
input int  InpMaxSignalsPerGroupShown = 6;
input bool InpRequireM1History = true;
input bool InpShowOnlyGroupsWithFinalStates = false;
input bool InpShowInvalidatedDoubleHunts = true;
input bool InpShowPrices = true;
input bool InpShowStopReferencePreview = true;

input bool InpEnableDrawing = true;
input bool InpClearPhase06ObjectsOnInit = true;
input bool InpClearPhase06ObjectsOnDeinit = false;
input bool InpDrawOnlyWhenChartIsHunterSymbol = false;
input bool InpDrawConfirmedTradeable = true;
input bool InpDrawInvalidatedDoubleHunts = true;
input bool InpDrawReferenceCycleAnchor = true;
input bool InpDrawConfirmationMarker = true;
input bool InpDrawTextLabel = true;
input int  InpLineWidth = 2;
input color InpBuyColor = clrLime;
input color InpSellColor = clrTomato;
input color InpInvalidatedColor = clrSilver;
input color InpTextColor = clrWhite;

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
   config.enable_drawing=InpEnableDrawing;
   config.clear_objects_on_init=InpClearPhase06ObjectsOnInit;
   config.clear_objects_on_deinit=InpClearPhase06ObjectsOnDeinit;
   config.draw_only_when_chart_is_hunter_symbol=InpDrawOnlyWhenChartIsHunterSymbol;
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
   config.enable_ledger=InpEnableLedger;
   config.ledger_use_common_files=InpLedgerUseCommonFiles;
   config.ledger_file_name=InpLedgerFileName;
   config.write_confirmed_to_ledger=InpWriteConfirmedToLedger;
   config.write_invalidated_to_ledger=InpWriteInvalidatedToLedger;
   config.use_file_duplicate_guard=InpUseFileDuplicateGuard;

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
