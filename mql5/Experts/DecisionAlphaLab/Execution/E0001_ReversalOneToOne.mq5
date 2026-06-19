//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0001 H0005 Reversal Fixed-R Executor       |
//| Exact H5 reversal: per-candle near-node limits + touch ledger       |
//+------------------------------------------------------------------+
#property strict
#property version   "1.27"
#property description "Execution module for H0005 reversal fixed-R: per-candle near-node touch limits with strict trading-session gate and node-zone touch ledger."

#include <Trade/Trade.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/M0002/DAL_M0002Engine.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecRisk.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecOrders.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecReversalOneToOne.mqh>

// Minimal public inputs. Everything else is fixed internally to keep the EA fast and testable.
input string InpSymbol = "";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 1500;

// H5 structure.
input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;

// Regime source.
enum ENUM_E0001RegimeBasis
{
   E0001_REGIME_LAST_COMPLETED_BRANCH = 0,
   E0001_REGIME_HUMAN_CONTEXT_COMBINED = 1
};

enum ENUM_E0001HumanContextSignal
{
   E0001_HUMAN_CONTEXT_NEUTRAL = 0,
   E0001_HUMAN_CONTEXT_REVERSAL = 1,
   E0001_HUMAN_CONTEXT_CONTINUATION = 2
};

input ENUM_E0001RegimeBasis InpRegimeBasis = E0001_REGIME_LAST_COMPLETED_BRANCH;
input ENUM_E0001HumanContextSignal InpHumanContextSignal = E0001_HUMAN_CONTEXT_NEUTRAL;

// Optional higher-timeframe regime filter. Off by default to keep current tests unchanged.
input bool InpUseHigherTimeframeRegimeFilter = false;
input ENUM_TIMEFRAMES InpHigherRegimeTimeframe = PERIOD_H1;

// Trading session. Broker time, strict: start <= time < end.
input bool InpUseTradingSessionFilter = true;
input int InpTradingStartHour = 0;
input int InpTradingStartMinute = 0;
input int InpTradingEndHour = 23;
input int InpTradingEndMinute = 59;

// Risk / target policy.
input long InpMagicNumber = 5001001;
input double InpRiskCash = 100.0;
input double InpRewardR = 1.0;
input bool InpUseFixedRExitIfCloser = false;
input bool InpAllowOppositeTouchBelowRewardR = true;

// E0001 limit grid and node touch ledger.
input int InpBuyLimitSlots = 3;
input int InpSellLimitSlots = 3;
input int InpTouchRevisitResetBufferPoints = 10;
input bool InpAllowNodeRevisitRearm = true;

// Internal fixed policy. These are intentionally not tester inputs.
int InpOutcomeCandleOffsetAfterExit = 0;
int InpBrokerUtcOffsetHours = 0;
int InpRegimeLookbackBars = 100;
bool InpUseClosedBarsOnly = true;
enum ENUM_E0001SessionClock
{
   E0001_SESSION_BROKER_TIME = 0,
   E0001_SESSION_GMT = 1
};
ENUM_E0001SessionClock InpTradingSessionClock = E0001_SESSION_BROKER_TIME;
bool InpDeletePendingsOutsideTradingSession = true;
bool InpH5ReportEnabled = false;
int InpH5ReportEveryNClosedBars = 1;
int InpH5ReportMaxSamples = 300;
int InpH5ReportMaxBarsAfterEntry = 0;
bool InpH5ReportPrintExamples = false;
bool InpTradingEnabled = true;
double InpCommissionPerLotRoundTurn = 0.0;
int InpMaxSimultaneousTrades = -1;
bool InpAllowOppositeTrades = true;
bool InpAllowMinLotIfRiskTooSmall = false;
int InpOrderExpirationMinutes = 0;
string InpOrderCommentPrefix = "DALR1";
enum ENUM_DALExecLogMode
{
   DAL_EXEC_LOG_NONE = 0,
   DAL_EXEC_LOG_ERRORS = 1,
   DAL_EXEC_LOG_ORDERS = 2,
   DAL_EXEC_LOG_VERBOSE = 3
};
int InpMaxZoneScanNodes = 0;
bool InpRefreshSetupsOnNewBarOnly = true;
bool InpManageOrdersEveryTick = false;
bool InpUpdateChartComment = false;
ENUM_DALExecLogMode InpLogMode = DAL_EXEC_LOG_ERRORS;
bool InpSyncManagedPendings = true;
bool InpCancelStaleManagedPendings = true;
bool InpCancelManagedPendingsAfterEntry = false;
bool InpUpdateExistingManagedPendings = true;
bool InpProtectPendingWhenPriceApproaches = true;
int InpPendingProtectDistancePoints = 20;
double InpPendingProtectStopFraction = 0.50;
bool InpAllowMarketCatchWhenAlreadyTouching = false;
bool InpMarketCatchRequiresPriceBeforeStop = true;

#define DAL_E0001_BUILD "1.27"

CTrade g_trade;
datetime g_last_open_bar_time = 0;
bool g_cache_ready = false;
string g_cache_reason = "not_initialized";
string g_last_cycle_signature = "";
DALExecReversalSetup g_cached_setups[];
int g_h5_report_refresh_counter = 0;
string g_last_h5_report_signature = "";
datetime g_last_outside_session_purge_bar_time = 0;

struct E0001TouchLock
{
   string comment;
   int node_id;
   int direction;
   double entry_price;
   double zone_lower;
   double zone_upper;
   bool locked;
   bool ever_touched;
};

E0001TouchLock g_touch_locks[];

string LabSymbol()
{
   if(InpSymbol == "")
      return _Symbol;
   return InpSymbol;
}

ENUM_TIMEFRAMES LabTimeframe()
{
   if(InpTimeframe == PERIOD_CURRENT)
      return (ENUM_TIMEFRAMES)_Period;
   return InpTimeframe;
}

bool LogErrors() { return (InpLogMode >= DAL_EXEC_LOG_ERRORS); }
bool LogOrders() { return (InpLogMode >= DAL_EXEC_LOG_ORDERS); }
bool LogVerbose() { return (InpLogMode >= DAL_EXEC_LOG_VERBOSE); }


int E0001_ClampInt(const int value, const int lo, const int hi)
{
   if(value < lo)
      return lo;
   if(value > hi)
      return hi;
   return value;
}

string E0001_TwoDigits(const int value)
{
   if(value < 10)
      return "0" + IntegerToString(value);
   return IntegerToString(value);
}

string E0001_FormatSessionMinute(const int minute_of_day)
{
   int safe_minute = E0001_ClampInt(minute_of_day, 0, 1439);
   int hh = safe_minute / 60;
   int mm = safe_minute % 60;
   return E0001_TwoDigits(hh) + ":" + E0001_TwoDigits(mm);
}

string E0001_FormatDateTime(const datetime value)
{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d.%02d.%02d %02d:%02d:%02d", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
}

bool E0001_IsTradingSessionOpen(string &reason)
{
   if(!InpUseTradingSessionFilter)
   {
      reason = "timeFilter=OFF";
      return true;
   }

   int start_hour = E0001_ClampInt(InpTradingStartHour, 0, 23);
   int start_minute = E0001_ClampInt(InpTradingStartMinute, 0, 59);
   int end_hour = E0001_ClampInt(InpTradingEndHour, 0, 23);
   int end_minute = E0001_ClampInt(InpTradingEndMinute, 0, 59);
   int start = start_hour * 60 + start_minute;
   int finish = end_hour * 60 + end_minute;

   datetime now_time = (InpTradingSessionClock == E0001_SESSION_GMT ? TimeGMT() : TimeCurrent());
   MqlDateTime dt;
   TimeToStruct(now_time, dt);
   int now_minute = dt.hour * 60 + dt.min;

   bool open = false;
   string window_type = "intraday_start_inclusive_end_exclusive";
   if(start == finish)
   {
      // Equal bounds are treated as all-day trading. This prevents a silent
      // no-trade trap when the user leaves both values at the same time.
      open = true;
      window_type = "all_day_equal_bounds";
   }
   else if(start < finish)
   {
      // Strict session window: trade from start, stop exactly at end.
      // Example 09:00 -> 17:00 means 09:00:00 <= now < 17:00:00.
      open = (now_minute >= start && now_minute < finish);
   }
   else
   {
      // Overnight strict window, for example 22:00 -> 02:00.
      open = (now_minute >= start || now_minute < finish);
      window_type = "overnight_start_inclusive_end_exclusive";
   }

   reason = StringFormat(
      "timeFilter=ON*clock=%s*now=%s*window=%s-%s*windowType=%s*open=%s",
      EnumToString(InpTradingSessionClock),
      E0001_FormatDateTime(now_time),
      E0001_FormatSessionMinute(start),
      E0001_FormatSessionMinute(finish),
      window_type,
      DAL_BoolToString(open)
   );
   return open;
}

string E0001_ManagedCommentPrefix()
{
   string prefix = InpOrderCommentPrefix;
   if(prefix == "")
      prefix = "DALR1";

   // Keep the managed identity short because many brokers truncate order comments.
   // Local helper avoids compile/runtime dependence on an include version mismatch.
   if(StringLen(prefix) > 10)
      prefix = StringSubstr(prefix, 0, 10);
   return prefix;
}

bool E0001_CheckMarketGeometry(
   const int direction,
   const double sl,
   const double tp,
   string &reason
)
{
   string symbol = LabSymbol();
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   int stops_level = (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL);
   double min_dist = MathMax(0.0, stops_level * point);

   if(point <= 0.0 || bid <= 0.0 || ask <= 0.0)
   {
      reason = "invalid_market_quote";
      return false;
   }

   if(direction > 0)
   {
      if(!(sl < ask && tp > ask))
      {
         reason = "invalid_buy_market_sl_tp_geometry";
         return false;
      }
      if((ask - sl) < min_dist || (tp - ask) < min_dist)
      {
         reason = "buy_market_sl_tp_too_close";
         return false;
      }
   }
   else if(direction < 0)
   {
      if(!(sl > bid && tp < bid))
      {
         reason = "invalid_sell_market_sl_tp_geometry";
         return false;
      }
      if((sl - bid) < min_dist || (bid - tp) < min_dist)
      {
         reason = "sell_market_sl_tp_too_close";
         return false;
      }
   }
   else
   {
      reason = "zero_direction";
      return false;
   }

   reason = "ok";
   return true;
}

bool E0001_PlaceMarketOrder(
   const int direction,
   const double volume,
   double sl,
   double tp,
   const string comment,
   string &reason
)
{
   string symbol = LabSymbol();
   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   sl = NormalizeDouble(sl, digits);
   tp = NormalizeDouble(tp, digits);

   if(!E0001_CheckMarketGeometry(direction, sl, tp, reason))
      return false;

   if(volume <= 0.0)
   {
      reason = "volume_zero";
      return false;
   }

   g_trade.SetExpertMagicNumber(InpMagicNumber);

   bool ok = false;
   if(direction > 0)
      ok = g_trade.Buy(volume, symbol, 0.0, sl, tp, comment);
   else
      ok = g_trade.Sell(volume, symbol, 0.0, sl, tp, comment);

   if(!ok)
   {
      reason = "market_send_failed_retcode_" + IntegerToString((int)g_trade.ResultRetcode()) + "_" + g_trade.ResultRetcodeDescription();
      return false;
   }

   reason = "ok_ticket_" + IntegerToString((int)g_trade.ResultOrder());
   return true;
}

double E0001_PriceTolerance()
{
   double point = SymbolInfoDouble(LabSymbol(), SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.00000001;
   return point * 0.5;
}

double E0001_VolumeTolerance()
{
   double step = SymbolInfoDouble(LabSymbol(), SYMBOL_VOLUME_STEP);
   if(step <= 0.0)
      step = 0.00000001;
   return step * 0.5;
}


void BuildM0001Config(DALM0001Config &config)
{
   DAL_M0001DefaultConfig(config);
   config.L = InpL;
   config.zone_ratio = InpZoneRatio;
   config.exit_gap = InpExitGap;
   config.consume_mode = InpConsumeMode;
   config.consume_on_touch = (InpConsumeMode == DAL_M0001_CONSUME_BY_TOUCH);
   config.max_events = 0;
   config.min_rtv = 0.0;
}

void BuildM0002Config(DALM0002Config &config)
{
   DAL_M0002DefaultConfig(config);
   config.measure_mode = DAL_M0002_MEASURE_EVENT_RTV;
   config.outcome_candle_offset_after_exit = MathMax(0, InpOutcomeCandleOffsetAfterExit);
   config.post_outcome_sample_bars = 0;
   config.use_event_length_for_sample = false;
   config.random_samples_per_event = 1;
   config.bootstrap_iterations = 0;
   config.permutation_iterations = 0;
   config.validation_splits = 1;
   config.broker_utc_offset_hours = InpBrokerUtcOffsetHours;
   config.regime_lookback_bars = MathMax(1, InpRegimeLookbackBars);
   config.print_group_session_regime = false;
   config.run_stress_suite = false;
   config.hard_random_candidates = 1;
   config.placebo_shift_bars = 1;
   config.nonoverlap_gap_bars = 0;
   config.block_bootstrap_iterations = 0;
   config.block_bootstrap_block_pairs = 1;
   config.consume_mode = InpConsumeMode;
   config.consume_on_touch = (InpConsumeMode == DAL_M0001_CONSUME_BY_TOUCH);
}

bool HasNewOpenCandle()
{
   datetime current_open = iTime(LabSymbol(), LabTimeframe(), 0);
   if(current_open <= 0)
      return false;

   if(g_last_open_bar_time <= 0)
   {
      g_last_open_bar_time = current_open;
      return true;
   }

   if(current_open == g_last_open_bar_time)
      return false;

   g_last_open_bar_time = current_open;
   return true;
}


bool E0001_ShouldRunOutsideSessionPurge()
{
   datetime current_open = iTime(LabSymbol(), LabTimeframe(), 0);
   if(current_open <= 0)
      current_open = TimeCurrent();

   if(g_last_outside_session_purge_bar_time == current_open)
      return false;

   g_last_outside_session_purge_bar_time = current_open;
   return true;
}

void UpdateComment(const string state)
{
   if(!InpUpdateChartComment)
      return;

   Comment(
      "DAL E0001 H5 REV R1 | build=", DAL_E0001_BUILD,
      " | state=", state,
      " | trading=", DAL_BoolToString(InpTradingEnabled), "\n",
      "symbol=", LabSymbol(),
      " tf=", EnumToString(LabTimeframe()),
      " risk=", DoubleToString(InpRiskCash, 2),
      " R=", DoubleToString(InpRewardR, 2),
      " max=", InpMaxSimultaneousTrades,
      " slots=", InpBuyLimitSlots, "/", InpSellLimitSlots,
      " setups=", ArraySize(g_cached_setups),
      " h5report=", DAL_BoolToString(InpH5ReportEnabled)
   );
}

void CopySetupsToCache(const DALExecReversalSetup &setups[], const string reason)
{
   int n = ArraySize(setups);
   ArrayResize(g_cached_setups, n);
   for(int i = 0; i < n; i++)
      g_cached_setups[i] = setups[i];
   g_cache_reason = reason;
   g_cache_ready = true;
}

void E0001_ClearSetupCache(const string reason)
{
   DALExecReversalSetup empty[];
   ArrayResize(empty, 0);
   CopySetupsToCache(empty, reason);
}



string E0001_RegimeOutcomeToString(const ENUM_DALM0002Outcome outcome)
{
   if(outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT)
      return "REVERSAL";
   if(outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT)
      return "CONTINUATION";
   return "UNKNOWN";
}

bool E0001_ResolveEffectiveRegime(DALM0002BranchSample &last_sample, const bool has_last_sample, string &reason)
{
   if(!has_last_sample)
   {
      reason = "no_last_branch";
      return false;
   }

   bool last_reversal = (last_sample.outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT);
   bool last_continuation = (last_sample.outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT);

   if(InpRegimeBasis == E0001_REGIME_LAST_COMPLETED_BRANCH)
   {
      reason = "regimeBasis=LAST_COMPLETED_BRANCH*last=" + E0001_RegimeOutcomeToString(last_sample.outcome);
      return last_reversal;
   }

   if(InpHumanContextSignal == E0001_HUMAN_CONTEXT_REVERSAL)
   {
      // Human/context override is intentionally explicit. It does not rebuild
      // M0001/M0002; it only changes the execution gate while the same node and
      // branch modules remain the source of structure.
      last_sample.outcome = DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT;
      reason = "regimeBasis=HUMAN_CONTEXT_COMBINED*human=REVERSAL*last=" + (last_reversal ? "REVERSAL" : (last_continuation ? "CONTINUATION" : "UNKNOWN"));
      return true;
   }

   if(InpHumanContextSignal == E0001_HUMAN_CONTEXT_CONTINUATION)
   {
      last_sample.outcome = DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT;
      reason = "regimeBasis=HUMAN_CONTEXT_COMBINED*human=CONTINUATION*last=" + (last_reversal ? "REVERSAL" : (last_continuation ? "CONTINUATION" : "UNKNOWN"));
      return false;
   }

   reason = "regimeBasis=HUMAN_CONTEXT_COMBINED*human=NEUTRAL*last=" + E0001_RegimeOutcomeToString(last_sample.outcome);
   return last_reversal;
}


bool E0001_PassesHigherTimeframeRegimeFilter(const ENUM_DALM0002Outcome required_outcome, string &reason)
{
   if(!InpUseHigherTimeframeRegimeFilter)
   {
      reason = "htfRegimeFilter=OFF";
      return true;
   }

   ENUM_TIMEFRAMES htf = InpHigherRegimeTimeframe;
   if(htf == PERIOD_CURRENT)
      htf = LabTimeframe();

   DALBar htf_bars[];
   int htf_bars_count = DAL_LoadBarsChronological(LabSymbol(), htf, InpBars, true, htf_bars);
   if(InpUseClosedBarsOnly && htf_bars_count > 1)
   {
      htf_bars_count--;
      ArrayResize(htf_bars, htf_bars_count);
   }

   if(htf_bars_count <= InpL * 2 + 10)
   {
      reason = "htfRegimeFilter=ON*tf=" + EnumToString(htf) + "*reason=not_enough_bars";
      return false;
   }

   DALM0001Config htf_m1;
   BuildM0001Config(htf_m1);

   DALLRuleNode htf_nodes[];
   int htf_nodes_count = DAL_DetectConfirmedStructuralNodes(htf_bars, htf_bars_count, htf_m1.L, htf_nodes);

   DALM0001Event htf_events[];
   int htf_events_count = DAL_M0001ComputeEvents(htf_bars, htf_bars_count, htf_nodes, htf_nodes_count, htf_m1, htf_events);

   DALM0002Config htf_m2;
   BuildM0002Config(htf_m2);

   DALM0002BranchSample htf_last_sample;
   int htf_last_event_index = -1;
   bool htf_has_last_sample = DAL_ExecFindLatestBranchSampleFast(htf_events, htf_events_count, htf_bars, htf_bars_count, 0, htf_m2, htf_last_sample, htf_last_event_index);
   if(!htf_has_last_sample)
   {
      reason = "htfRegimeFilter=ON*tf=" + EnumToString(htf) + "*reason=no_last_branch";
      return false;
   }

   bool pass = (htf_last_sample.outcome == required_outcome);
   reason = "htfRegimeFilter=ON*tf=" + EnumToString(htf)
      + "*last=" + E0001_RegimeOutcomeToString(htf_last_sample.outcome)
      + "*required=" + E0001_RegimeOutcomeToString(required_outcome)
      + "*pass=" + DAL_BoolToString(pass);
   return pass;
}


void E0001_MaybePrintH5ResearchReport(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Event &events[],
   const int events_count,
   const DALM0002Config &m2,
   const string trigger
)
{
   if(!InpH5ReportEnabled)
      return;

   int every_n = InpH5ReportEveryNClosedBars;
   if(every_n < 1)
      every_n = 1;
   g_h5_report_refresh_counter++;
   if((g_h5_report_refresh_counter % every_n) != 0)
      return;

   DALExecH5FixedRReport report;
   string reason = "";
   bool ok = DAL_ExecBuildH5ReversalFixedRResearchReport(
      LabSymbol(),
      bars,
      bars_count,
      nodes,
      nodes_count,
      events,
      events_count,
      m2,
      InpZoneRatio,
      InpRewardR,
      E0001_ManagedCommentPrefix(),
      InpUseFixedRExitIfCloser,
      InpAllowOppositeTouchBelowRewardR,
      InpBuyLimitSlots,
      InpSellLimitSlots,
      InpMaxZoneScanNodes,
      InpH5ReportMaxSamples,
      InpH5ReportMaxBarsAfterEntry,
      report,
      reason
   );

   string log = DAL_ExecH5FixedRReportToLog(report);
   string signature = IntegerToString(report.sample_count) + ":" + IntegerToString(report.reversal_sample_count) + ":" + IntegerToString(report.planned_trades) + ":" + IntegerToString(report.filled_trades) + ":" + IntegerToString(report.target_hits) + ":" + IntegerToString(report.stop_hits) + ":" + reason;

   if(LogOrders() && (InpH5ReportEveryNClosedBars <= 1 || signature != g_last_h5_report_signature))
   {
      g_last_h5_report_signature = signature;
      Print("DAL_E0001_H5_RESEARCH_REPORT *** build=", DAL_E0001_BUILD,
         "*ok=", DAL_BoolToString(ok),
         "*trigger=", trigger,
         "*reason=", reason,
         "*", log);
   }

   if(InpH5ReportPrintExamples && LogVerbose())
   {
      Print("DAL_E0001_H5_RESEARCH_NOTE *** build=", DAL_E0001_BUILD,
         "*model=LAST_COMPLETED_BRANCH_then_nearest_LOW_buys_and_HIGH_sells",
         "*entryModel=buy_zone_upper_plus_spread_sell_zone_lower",
         "*stopModel=buy_zone_lower_sell_zone_upper_plus_spread",
         "*tpModel=first_opposite_node_touch_optional_fixed_r_exit",
         "*ambiguityPolicy=same_bar_tp_and_sl_counted_as_ambiguous_and_conservative_stop");
   }
}

bool BuildCurrentSetups(DALExecReversalSetup &setups[], string &reason)
{
   ArrayResize(setups, 0);
   reason = "not_built";

   string session_reason = "";
   if(!E0001_IsTradingSessionOpen(session_reason))
   {
      reason = "trading_session_closed*" + session_reason;
      return false;
   }

   DALBar bars[];
   int bars_count = DAL_LoadBarsChronological(LabSymbol(), LabTimeframe(), InpBars, true, bars);
   if(InpUseClosedBarsOnly && bars_count > 1)
   {
      bars_count--;
      ArrayResize(bars, bars_count);
   }
   if(bars_count <= InpL * 2 + 10)
   {
      reason = "not_enough_bars";
      return false;
   }

   DALM0001Config m1;
   BuildM0001Config(m1);

   DALLRuleNode nodes[];
   int nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, m1.L, nodes);

   DALM0001Event events[];
   int events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, m1, events);

   DALM0002Config m2;
   BuildM0002Config(m2);

   E0001_MaybePrintH5ResearchReport(bars, bars_count, nodes, nodes_count, events, events_count, m2, "cache_refresh");

   DALM0002BranchSample last_sample;
   int last_event_index = -1;
   bool has_last_sample = DAL_ExecFindLatestBranchSampleFast(events, events_count, bars, bars_count, 0, m2, last_sample, last_event_index);

   string regime_reason = "";
   if(!E0001_ResolveEffectiveRegime(last_sample, has_last_sample, regime_reason))
   {
      reason = regime_reason;
      return false;
   }


   string htf_regime_reason = "";
   if(!E0001_PassesHigherTimeframeRegimeFilter(DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT, htf_regime_reason))
   {
      reason = regime_reason + "*" + htf_regime_reason;
      return false;
   }

   int n = DAL_ExecCollectH5ReversalRSetups(
      LabSymbol(),
      bars,
      bars_count,
      nodes,
      nodes_count,
      events,
      events_count,
      last_sample,
      has_last_sample,
      m1.zone_ratio,
      InpRewardR,
      E0001_ManagedCommentPrefix(),
      InpUseFixedRExitIfCloser,
      InpAllowOppositeTouchBelowRewardR,
      InpBuyLimitSlots,
      InpSellLimitSlots,
      InpMaxZoneScanNodes,
      setups,
      reason
   );

   return (n > 0);
}

bool RefreshSetupCacheIfNeeded()
{
   bool refresh = !g_cache_ready;
   if(!refresh)
   {
      if(!InpRefreshSetupsOnNewBarOnly)
         refresh = true;
      else if(HasNewOpenCandle())
         refresh = true;
   }

   if(!refresh)
      return false;

   DALExecReversalSetup setups[];
   string reason = "";
   bool ok = BuildCurrentSetups(setups, reason);
   if(!ok)
      ArrayResize(setups, 0);

   CopySetupsToCache(setups, reason);

   if(LogVerbose())
      Print("DAL_E0001_CACHE *** build=", DAL_E0001_BUILD, "*setups=", ArraySize(g_cached_setups), "*reason=", reason);

   return true;
}

bool SetupCommentInCache(const string comment)
{
   for(int i = 0; i < ArraySize(g_cached_setups); i++)
   {
      if(g_cached_setups[i].valid && g_cached_setups[i].comment == comment)
         return true;
   }
   return false;
}

bool FindSetupInCacheByComment(const string comment, DALExecReversalSetup &setup)
{
   DAL_ExecResetReversalSetup(setup);
   for(int i = 0; i < ArraySize(g_cached_setups); i++)
   {
      if(g_cached_setups[i].valid && g_cached_setups[i].comment == comment)
      {
         setup = g_cached_setups[i];
         return true;
      }
   }
   return false;
}

int E0001_FindTouchLockIndexByKey(const int node_id, const int direction, const string comment)
{
   // Primary identity is the structural node, not the order comment. Comments can
   // change with reward/prefix or be broker-truncated; H5 touch state belongs to
   // the node + side until that node's zone is truly exited.
   if(node_id >= 0 && direction != 0)
   {
      for(int i = 0; i < ArraySize(g_touch_locks); i++)
      {
         if(g_touch_locks[i].node_id == node_id && g_touch_locks[i].direction == direction)
            return i;
      }
   }

   if(comment != "")
   {
      for(int i = 0; i < ArraySize(g_touch_locks); i++)
      {
         if(g_touch_locks[i].comment == comment)
            return i;
      }
   }

   return -1;
}

int E0001_FindTouchLockIndex(const string comment)
{
   return E0001_FindTouchLockIndexByKey(-1, 0, comment);
}

void E0001_SetNodeTouchLock(
   const string comment,
   const int node_id,
   const int direction,
   const double entry_price,
   const double zone_lower,
   const double zone_upper
)
{
   if(comment == "" && node_id < 0)
      return;

   int idx = E0001_FindTouchLockIndexByKey(node_id, direction, comment);
   bool was_locked = false;
   if(idx < 0)
   {
      idx = ArraySize(g_touch_locks);
      ArrayResize(g_touch_locks, idx + 1);
      g_touch_locks[idx].comment = comment;
      g_touch_locks[idx].node_id = node_id;
      g_touch_locks[idx].direction = direction;
      g_touch_locks[idx].entry_price = entry_price;
      g_touch_locks[idx].zone_lower = zone_lower;
      g_touch_locks[idx].zone_upper = zone_upper;
      g_touch_locks[idx].locked = false;
      g_touch_locks[idx].ever_touched = false;
   }
   else
   {
      was_locked = g_touch_locks[idx].locked;
   }

   // Preserve node identity and the actual touched zone. If the cache later
   // recomputes a slightly different live zone, do not move the lock boundary
   // inside the same touch; otherwise the EA may re-arm too early. Boundaries
   // are refreshed only when this node is currently unlocked, i.e. at the start
   // of a fresh touch/revisit episode.
   if(g_touch_locks[idx].comment == "")
      g_touch_locks[idx].comment = comment;
   g_touch_locks[idx].node_id = node_id;
   g_touch_locks[idx].direction = direction;
   if(!was_locked)
   {
      g_touch_locks[idx].entry_price = entry_price;
      if(zone_lower > 0.0 && zone_upper > 0.0 && zone_upper >= zone_lower)
      {
         g_touch_locks[idx].zone_lower = zone_lower;
         g_touch_locks[idx].zone_upper = zone_upper;
      }
   }
   g_touch_locks[idx].locked = true;
   g_touch_locks[idx].ever_touched = true;
}

void E0001_SetTouchLockFromSetup(const DALExecReversalSetup &setup)
{
   E0001_SetNodeTouchLock(setup.comment, setup.node_id, setup.direction, setup.entry_price, setup.zone_lower, setup.zone_upper);
}

// Legacy fallback used only when a trade transaction cannot be mapped back to a
// current setup. It still locks by comment, but normal execution locks by node.
void E0001_SetTouchLock(const string comment, const int direction, const double entry_price)
{
   E0001_SetNodeTouchLock(comment, -1, direction, entry_price, entry_price, entry_price);
}

bool E0001_TouchLockedSetup(const DALExecReversalSetup &setup)
{
   int idx = E0001_FindTouchLockIndexByKey(setup.node_id, setup.direction, setup.comment);
   return (idx >= 0 && g_touch_locks[idx].locked);
}

bool E0001_TouchLocked(const string comment)
{
   int idx = E0001_FindTouchLockIndex(comment);
   return (idx >= 0 && g_touch_locks[idx].locked);
}

void E0001_UpdateTouchRevisitLocks()
{
   if(!InpAllowNodeRevisitRearm)
      return;

   string symbol = LabSymbol();
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.00000001;

   double buffer = MathMax(0.0, (double)InpTouchRevisitResetBufferPoints) * point;

   for(int i = 0; i < ArraySize(g_touch_locks); i++)
   {
      if(!g_touch_locks[i].locked)
         continue;

      int direction = g_touch_locks[i].direction;
      double zone_lower = g_touch_locks[i].zone_lower;
      double zone_upper = g_touch_locks[i].zone_upper;
      double entry = g_touch_locks[i].entry_price;

      // Fallback for older comment-only locks. Normal H5 locks store the actual
      // node zone, so unlock is based on exiting the whole node range, not only
      // moving a few points away from the limit entry.
      if(zone_lower <= 0.0 || zone_upper <= 0.0 || zone_upper < zone_lower)
      {
         DALExecReversalSetup setup;
         if(FindSetupInCacheByComment(g_touch_locks[i].comment, setup))
         {
            zone_lower = setup.zone_lower;
            zone_upper = setup.zone_upper;
            entry = setup.entry_price;
            direction = setup.direction;
         }
         else
         {
            zone_lower = entry;
            zone_upper = entry;
         }
      }

      // Buy node: touch happens from above into a LOW-node zone. Re-arm only
      // after ask has exited above the full zone. A move deeper below the zone
      // is node consumption, not a valid same-node revisit.
      if(direction > 0 && ask > zone_upper + buffer)
      {
         g_touch_locks[i].locked = false;
         if(LogVerbose())
            Print("DAL_E0001_NODE_TOUCH_UNLOCK *** build=", DAL_E0001_BUILD,
               "*dir=buy*nodeId=", g_touch_locks[i].node_id,
               "*zoneUpper=", DoubleToString(zone_upper, _Digits),
               "*zoneLower=", DoubleToString(zone_lower, _Digits),
               "*bufferPoints=", InpTouchRevisitResetBufferPoints,
               "*comment=", g_touch_locks[i].comment);
      }
      // Sell node: touch happens from below into a HIGH-node zone. Re-arm only
      // after bid has exited below the full zone. A move above the zone is node
      // consumption, not a valid same-node revisit.
      else if(direction < 0 && bid < zone_lower - buffer)
      {
         g_touch_locks[i].locked = false;
         if(LogVerbose())
            Print("DAL_E0001_NODE_TOUCH_UNLOCK *** build=", DAL_E0001_BUILD,
               "*dir=sell*nodeId=", g_touch_locks[i].node_id,
               "*zoneUpper=", DoubleToString(zone_upper, _Digits),
               "*zoneLower=", DoubleToString(zone_lower, _Digits),
               "*bufferPoints=", InpTouchRevisitResetBufferPoints,
               "*comment=", g_touch_locks[i].comment);
      }
   }
}

void E0001_PruneTouchLocksToManagedPrefix()
{
   string prefix = E0001_ManagedCommentPrefix();
   for(int i = ArraySize(g_touch_locks) - 1; i >= 0; i--)
   {
      // Keep locks for the current managed prefix even when the node is not in
      // the latest 3+3 cache. A touch episode can temporarily fall out of the
      // near-node cache, during continuation, outside session, or while another
      // node is closer. Dropping that lock would allow a duplicate limit inside
      // the same touch. The lock is released only by a real exit from the touch
      // zone in E0001_UpdateTouchRevisitLocks().
      if(DAL_ExecOrderCommentMatchesPrefix(g_touch_locks[i].comment, prefix))
         continue;

      for(int j = i; j < ArraySize(g_touch_locks) - 1; j++)
         g_touch_locks[j] = g_touch_locks[j + 1];
      ArrayResize(g_touch_locks, ArraySize(g_touch_locks) - 1);
   }
}

bool E0001_FindPendingByComment(const string comment, DALExecPendingOrder &pending)
{
   DAL_ExecResetPendingOrder(pending);
   for(int i = 0; i < OrdersTotal(); i++)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0 || !OrderSelect(ticket))
         continue;
      if(OrderGetString(ORDER_SYMBOL) != LabSymbol())
         continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != InpMagicNumber)
         continue;
      if(OrderGetString(ORDER_COMMENT) != comment)
         continue;
      if(!DAL_ExecReadPendingOrder(ticket, pending))
         continue;
      return true;
   }
   return false;
}

bool E0001_PositionExistsByComment(const string comment)
{
   for(int i = 0; i < PositionsTotal(); i++)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != LabSymbol())
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != InpMagicNumber)
         continue;
      if(PositionGetString(POSITION_COMMENT) == comment)
         return true;
   }
   return false;
}

bool E0001_PendingNeedsUpdate(const DALExecPendingOrder &pending, const DALExecReversalSetup &setup, const DALExecRiskSizing &risk, bool &volume_changed)
{
   volume_changed = (MathAbs(pending.volume - risk.volume) > E0001_VolumeTolerance());

   double tol = E0001_PriceTolerance();
   if(MathAbs(pending.price - setup.entry_price) > tol)
      return true;
   if(MathAbs(pending.sl - setup.stop_price) > tol)
      return true;
   if(MathAbs(pending.tp - setup.tp_price) > tol)
      return true;

   return volume_changed;
}

bool E0001_ModifyPendingToSetup(const DALExecPendingOrder &pending, const DALExecReversalSetup &setup, string &reason)
{
   double entry = setup.entry_price;
   double sl = setup.stop_price;
   double tp = setup.tp_price;
   DAL_ExecNormalizePrices(LabSymbol(), entry, sl, tp);

   if(!DAL_ExecCheckLimitGeometry(LabSymbol(), setup.direction, entry, sl, tp, reason))
      return false;

   datetime expiration = 0;
   ENUM_ORDER_TYPE_TIME type_time = ORDER_TIME_GTC;
   if(InpOrderExpirationMinutes > 0)
   {
      type_time = ORDER_TIME_SPECIFIED;
      expiration = TimeCurrent() + InpOrderExpirationMinutes * 60;
   }

   g_trade.SetExpertMagicNumber(InpMagicNumber);
   if(!g_trade.OrderModify(pending.ticket, entry, sl, tp, type_time, expiration, 0.0))
   {
      reason = "modify_failed_retcode_" + IntegerToString((int)g_trade.ResultRetcode()) + "_" + g_trade.ResultRetcodeDescription();
      return false;
   }

   reason = "ok_modified_" + IntegerToString((int)pending.ticket);
   return true;
}

bool PendingIsProtectedNearMarket(const DALExecPendingOrder &pending)
{
   if(!pending.found || !InpProtectPendingWhenPriceApproaches)
      return false;

   double point = SymbolInfoDouble(LabSymbol(), SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.00000001;

   double stop_distance = MathAbs(pending.price - pending.sl);
   double protect_distance = MathMax(0.0, (double)InpPendingProtectDistancePoints) * point;
   if(stop_distance > 0.0 && InpPendingProtectStopFraction > 0.0)
      protect_distance = MathMax(protect_distance, stop_distance * InpPendingProtectStopFraction);

   if(protect_distance <= 0.0)
      return false;

   double market_distance = DAL_ExecPendingDistanceToMarket(LabSymbol(), pending.direction, pending.price);
   return (market_distance <= protect_distance);
}

bool HasManagedPosition()
{
   string managed_prefix = E0001_ManagedCommentPrefix();
   int total = PositionsTotal();
   for(int i = 0; i < total; i++)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != LabSymbol())
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != InpMagicNumber)
         continue;
      if(!DAL_ExecOrderCommentMatchesPrefix(PositionGetString(POSITION_COMMENT), managed_prefix))
         continue;
      return true;
   }
   return false;
}

void SyncStaleManagedPendings()
{
   if(!InpSyncManagedPendings || !InpCancelStaleManagedPendings)
      return;

   string managed_prefix = E0001_ManagedCommentPrefix();
   bool managed_position_open = (InpCancelManagedPendingsAfterEntry && HasManagedPosition());
   bool no_current_reversal_setups = (ArraySize(g_cached_setups) <= 0);
   int deleted = 0;

   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0 || !OrderSelect(ticket))
         continue;
      if(OrderGetString(ORDER_SYMBOL) != LabSymbol())
         continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != InpMagicNumber)
         continue;

      ENUM_ORDER_TYPE type = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
      if(!DAL_ExecOrderIsPendingLimit(type))
         continue;

      string comment = OrderGetString(ORDER_COMMENT);
      if(!DAL_ExecOrderCommentMatchesPrefix(comment, managed_prefix))
         continue;

      if(!managed_position_open && SetupCommentInCache(comment))
         continue;

      DALExecPendingOrder pending;
      if(!DAL_ExecReadPendingOrder(ticket, pending))
         continue;

      // In continuation/non-reversal regime everything must be removed. Protection
      // is only for active reversal setups that are close to being filled.
      if(!managed_position_open && !no_current_reversal_setups && PendingIsProtectedNearMarket(pending))
         continue;

      string delete_reason = "";
      string sync_reason = managed_position_open ? "managed_position_open_cancel_unused_candidate" : "stale_or_non_reversal_regime";
      if(DAL_ExecDeletePendingOrder(ticket, g_trade, delete_reason))
      {
         deleted++;
         if(LogOrders())
            Print("DAL_E0001_PENDING_DELETE *** build=", DAL_E0001_BUILD, "*ticket=", (long)ticket, "*reason=", sync_reason, "*comment=", comment);
      }
      else if(LogErrors())
      {
         Print("DAL_E0001_PENDING_DELETE_FAIL *** build=", DAL_E0001_BUILD, "*ticket=", (long)ticket, "*reason=", delete_reason, "*comment=", comment);
      }
   }

   if(no_current_reversal_setups)
      E0001_PruneTouchLocksToManagedPrefix();

   if(deleted > 0 && LogVerbose())
      Print("DAL_E0001_PENDING_SYNC *** build=", DAL_E0001_BUILD, "*deleted=", deleted);
}

int E0001_ForceDeleteManagedPendingLimits(const string context, string &summary)
{
   int deleted = 0;
   int failed = 0;
   summary = "ok";
   string managed_prefix = E0001_ManagedCommentPrefix();

   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0 || !OrderSelect(ticket))
         continue;
      if(OrderGetString(ORDER_SYMBOL) != LabSymbol())
         continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != InpMagicNumber)
         continue;

      ENUM_ORDER_TYPE type = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
      if(!DAL_ExecOrderIsPendingLimit(type))
         continue;

      string comment = OrderGetString(ORDER_COMMENT);
      if(!DAL_ExecOrderCommentMatchesPrefix(comment, managed_prefix))
         continue;

      string delete_reason = "";
      if(DAL_ExecDeletePendingOrder(ticket, g_trade, delete_reason))
      {
         deleted++;
         if(LogOrders())
            Print("DAL_E0001_PENDING_FORCE_DELETE *** build=", DAL_E0001_BUILD,
               "*context=", context,
               "*ticket=", (long)ticket,
               "*comment=", comment,
               "*reason=", delete_reason);
      }
      else
      {
         failed++;
         summary = delete_reason;
         if(LogErrors())
            Print("DAL_E0001_PENDING_FORCE_DELETE_FAIL *** build=", DAL_E0001_BUILD,
               "*context=", context,
               "*ticket=", (long)ticket,
               "*comment=", comment,
               "*reason=", delete_reason);
      }
   }

   summary = "deleted=" + IntegerToString(deleted) + "*failed=" + IntegerToString(failed) + "*lastReason=" + summary;
   return deleted;
}

bool MarketIsAlreadyTouchingSetup(const DALExecReversalSetup &setup, double &market_entry)
{
   market_entry = 0.0;
   double bid = SymbolInfoDouble(LabSymbol(), SYMBOL_BID);
   double ask = SymbolInfoDouble(LabSymbol(), SYMBOL_ASK);
   if(bid <= 0.0 || ask <= 0.0 || !setup.valid)
      return false;

   if(setup.direction > 0)
   {
      market_entry = ask;
      if(!(ask <= setup.entry_price))
         return false;
      if(InpMarketCatchRequiresPriceBeforeStop && !(ask > setup.stop_price))
         return false;
      return true;
   }

   if(setup.direction < 0)
   {
      market_entry = bid;
      if(!(bid >= setup.entry_price))
         return false;
      if(InpMarketCatchRequiresPriceBeforeStop && !(bid < setup.stop_price))
         return false;
      return true;
   }

   return false;
}


void E0001_LockCurrentTouchEpisode(const DALExecReversalSetup &setup, const string context, const double market_entry)
{
   E0001_SetTouchLockFromSetup(setup);
   if(LogOrders())
   {
      Print("DAL_E0001_NODE_TOUCH_EPISODE_LOCK *** build=", DAL_E0001_BUILD,
         "*context=", context,
         "*dir=", setup.direction,
         "*marketEntry=", DoubleToString(market_entry, _Digits),
         "*entry=", DoubleToString(setup.entry_price, _Digits),
         "*zoneLower=", DoubleToString(setup.zone_lower, _Digits),
         "*zoneUpper=", DoubleToString(setup.zone_upper, _Digits),
         "*unlockBufferPoints=", InpTouchRevisitResetBufferPoints,
         "*comment=", setup.comment);
   }
}

bool SetupLimitOrderableNow(const DALExecReversalSetup &setup, string &reason)
{
   double entry = setup.entry_price;
   double sl = setup.stop_price;
   double tp = setup.tp_price;
   DAL_ExecNormalizePrices(LabSymbol(), entry, sl, tp);
   return DAL_ExecCheckLimitGeometry(LabSymbol(), setup.direction, entry, sl, tp, reason);
}

bool PlaceSetupLimitOrder(const DALExecReversalSetup &setup, const DALExecRiskSizing &risk, string &order_reason)
{
   order_reason = "dry_run";
   if(!InpTradingEnabled)
      return false;

   return DAL_ExecPlaceLimitOrder(
      LabSymbol(),
      InpMagicNumber,
      setup.direction,
      risk.volume,
      setup.entry_price,
      setup.stop_price,
      setup.tp_price,
      setup.comment,
      InpOrderExpirationMinutes,
      g_trade,
      order_reason
   );
}

bool PlaceSetupMarketCatch(const DALExecReversalSetup &setup, const double market_entry, string &order_reason, DALExecRiskSizing &risk)
{
   order_reason = "market_catch_disabled";
   DAL_ExecResetRiskSizing(risk);

   if(!InpAllowMarketCatchWhenAlreadyTouching)
      return false;

   double stop_distance = MathAbs(market_entry - setup.stop_price);
   if(stop_distance <= 0.0)
   {
      order_reason = "market_catch_zero_stop_distance";
      return false;
   }

   string tp_model = "";
   string tp_reject_reason = "";
   double tp = 0.0;
   double fixed_r_tp = 0.0;
   double opposite_touch_r = 0.0;
   if(!DAL_ExecResolveTpForActualEntry(setup, market_entry, InpUseFixedRExitIfCloser, InpAllowOppositeTouchBelowRewardR, tp, fixed_r_tp, opposite_touch_r, tp_model, tp_reject_reason))
   {
      order_reason = "market_catch_tp_reject_" + tp_reject_reason;
      return false;
   }
   bool risk_ok = DAL_ExecCalculateRiskVolume(
      LabSymbol(),
      market_entry,
      setup.stop_price,
      InpRiskCash,
      InpCommissionPerLotRoundTurn,
      InpAllowMinLotIfRiskTooSmall,
      risk
   );
   if(!risk_ok)
   {
      order_reason = "market_catch_risk_reject_" + risk.reason;
      return false;
   }

   order_reason = "dry_run_market_catch";
   if(!InpTradingEnabled)
      return false;

   return E0001_PlaceMarketOrder(
      setup.direction,
      risk.volume,
      setup.stop_price,
      tp,
      setup.comment,
      order_reason
   );
}

void TryPlaceCachedSetups()
{
   string session_reason = "";
   if(!E0001_IsTradingSessionOpen(session_reason))
   {
      E0001_ClearSetupCache("trading_session_closed*" + session_reason);
      string force_delete_summary = "disabled";
      int force_deleted = 0;
      if(InpDeletePendingsOutsideTradingSession)
         force_deleted = E0001_ForceDeleteManagedPendingLimits("outside_trading_session_try_place_guard", force_delete_summary);
      if(LogOrders())
         Print("DAL_E0001_TIME_FILTER *** build=", DAL_E0001_BUILD,
            "*action=try_place_guard_blocked",
            "*forceDeleted=", force_deleted,
            "*deleteSummary=", force_delete_summary,
            "*", session_reason);
      UpdateComment("trading_session_closed");
      return;
   }

   E0001_UpdateTouchRevisitLocks();
   SyncStaleManagedPendings();

   int setup_count = ArraySize(g_cached_setups);
   if(setup_count <= 0)
   {
      if(LogVerbose())
         Print("DAL_E0001_SKIP *** build=", DAL_E0001_BUILD, "*reason=", g_cache_reason, "*mode=h5_reversal_fixed_r_touch_cache");
      UpdateComment("no_h5_r1_setup_" + g_cache_reason);
      return;
   }

   int submitted = 0;
   int modified = 0;
   int skipped_existing = 0;
   int skipped_touch_lock = 0;
   int skipped_blocked = 0;
   int skipped_risk = 0;
   int skipped_market_catch = 0;
   int skipped_update = 0;
   int skipped_geometry = 0;

   for(int i = 0; i < setup_count; i++)
   {
      DALExecReversalSetup setup = g_cached_setups[i];
      if(!setup.valid)
         continue;

      if(E0001_PositionExistsByComment(setup.comment))
      {
         E0001_SetTouchLockFromSetup(setup);
         skipped_existing++;
         continue;
      }

      if(E0001_TouchLockedSetup(setup))
      {
         skipped_touch_lock++;
         if(LogVerbose())
            Print("DAL_E0001_SKIP *** build=", DAL_E0001_BUILD, "*reason=node_touch_locked_wait_zone_exit*comment=", setup.comment);
         continue;
      }


      DALExecRiskSizing risk;
      bool risk_ok = DAL_ExecCalculateRiskVolume(
         LabSymbol(),
         setup.entry_price,
         setup.stop_price,
         InpRiskCash,
         InpCommissionPerLotRoundTurn,
         InpAllowMinLotIfRiskTooSmall,
         risk
      );

      if(!risk_ok)
      {
         skipped_risk++;
         if(LogErrors())
            Print("DAL_E0001_RISK_REJECT *** build=", DAL_E0001_BUILD, "*reason=", risk.reason, "*entry=", DoubleToString(setup.entry_price, _Digits), "*stop=", DoubleToString(setup.stop_price, _Digits), "*comment=", setup.comment);
         continue;
      }

      DALExecPendingOrder pending;
      if(E0001_FindPendingByComment(setup.comment, pending))
      {
         bool volume_changed = false;
         bool needs_update = E0001_PendingNeedsUpdate(pending, setup, risk, volume_changed);
         if(!needs_update || !InpUpdateExistingManagedPendings)
         {
            skipped_existing++;
            continue;
         }

         if(PendingIsProtectedNearMarket(pending))
         {
            skipped_update++;
            if(LogVerbose())
               Print("DAL_E0001_PENDING_UPDATE_SKIP *** build=", DAL_E0001_BUILD, "*reason=protected_near_market*comment=", setup.comment);
            continue;
         }

         string update_reason = "";
         bool update_ok = false;
         if(volume_changed)
         {
            if(DAL_ExecDeletePendingOrder(pending.ticket, g_trade, update_reason))
            {
               string order_reason = "";
               update_ok = PlaceSetupLimitOrder(setup, risk, order_reason);
               update_reason = update_reason + "+" + order_reason;
               if(update_ok)
                  modified++;
            }
         }
         else
         {
            update_ok = E0001_ModifyPendingToSetup(pending, setup, update_reason);
            if(update_ok)
               modified++;
         }

         if(LogOrders() || (InpTradingEnabled && !update_ok && LogErrors()))
         {
            Print(
               "DAL_E0001_PENDING_UPDATE *** build=", DAL_E0001_BUILD,
               "*ok=", DAL_BoolToString(update_ok),
               "*reason=", update_reason,
               "*volumeChanged=", DAL_BoolToString(volume_changed),
               "*dir=", setup.direction,
               "*entry=", DoubleToString(setup.entry_price, _Digits),
               "*sl=", DoubleToString(setup.stop_price, _Digits),
               "*tp=", DoubleToString(setup.tp_price, _Digits),
               "*tpModel=", setup.tp_model,
               "*fixedRTp=", DoubleToString(setup.fixed_r_tp_price, _Digits),
               "*oppositeTouchTp=", DoubleToString(setup.opposite_touch_tp_price, _Digits),
               "*oppositeTouchNode=", setup.opposite_touch_node_id,
            "*oppositeTouchR=", DoubleToString(setup.opposite_touch_r, 4),
               "*rawEntryEdge=", DoubleToString(setup.raw_entry_edge, _Digits),
               "*rawStopEdge=", DoubleToString(setup.raw_stop_edge, _Digits),
               "*spread=", DoubleToString(setup.spread_price, _Digits),
               "*comment=", setup.comment
            );
         }

         if(!update_ok)
            skipped_update++;
         continue;
      }

      string exposure_reason = "";
      if(!DAL_ExecCanOpenDirection(LabSymbol(), InpMagicNumber, setup.direction, InpMaxSimultaneousTrades, InpAllowOppositeTrades, exposure_reason))
      {
         skipped_blocked++;
         if(LogVerbose())
            Print("DAL_E0001_SKIP *** build=", DAL_E0001_BUILD, "*reason=", exposure_reason, "*direction=", setup.direction, "*comment=", setup.comment);
         if(StringFind(exposure_reason, "max_simultaneous", 0) >= 0)
            break;
         continue;
      }

      double market_entry = 0.0;
      bool already_touching = MarketIsAlreadyTouchingSetup(setup, market_entry);
      if(already_touching)
      {
         // This is the critical H5 touch/revisit rule: once the market has
         // entered the planned touch edge, this touch episode is consumed for
         // order planting. Do not delete/recreate another limit while price is
         // still inside the same touch. The node can arm again only after the
         // price exits the edge by InpTouchRevisitResetBufferPoints and then
         // revisits it.
         E0001_LockCurrentTouchEpisode(setup, "market_already_inside_touch_before_new_limit", market_entry);

         DALExecRiskSizing market_risk;
         string market_reason = "";
         bool market_ok = PlaceSetupMarketCatch(setup, market_entry, market_reason, market_risk);
         if(market_ok)
            submitted++;
         else
            skipped_market_catch++;

         if(LogOrders() || (InpTradingEnabled && !market_ok && LogErrors()))
         {
            Print(
               "DAL_E0001_MARKET_CATCH *** build=", DAL_E0001_BUILD,
               "*sent=", DAL_BoolToString(market_ok),
               "*reason=", market_reason,
               "*touchLocked=", DAL_BoolToString(true),
               "*dir=", setup.direction,
               "*entry=", DoubleToString(market_entry, _Digits),
               "*sl=", DoubleToString(setup.stop_price, _Digits),
               "*rewardR=", DoubleToString(setup.reward_r, 4),
               "*vol=", DoubleToString(market_risk.volume, 4),
               "*comment=", setup.comment
            );
         }
         continue;
      }

      string geometry_reason = "";
      if(!SetupLimitOrderableNow(setup, geometry_reason))
      {
         // The setup cache is structural, not orderability-filtered. Price may
         // cross a touch edge between cache build and order send. In exact
         // limit-only mode we do not chase with market; we log the miss and wait
         // for the next orderable revisit.
         skipped_geometry++;
         if(LogVerbose())
            Print("DAL_E0001_SKIP *** build=", DAL_E0001_BUILD, "*reason=", geometry_reason, "*mode=limit_not_orderable_now*dir=", setup.direction, "*entry=", DoubleToString(setup.entry_price, _Digits), "*comment=", setup.comment);
         continue;
      }

      string order_reason = "";
      bool order_ok = PlaceSetupLimitOrder(setup, risk, order_reason);
      if(order_ok)
         submitted++;

      if(LogOrders() || (InpTradingEnabled && !order_ok && LogErrors()))
      {
         Print(
            "DAL_E0001_LIMIT_ORDER *** build=", DAL_E0001_BUILD,
            "*sent=", DAL_BoolToString(order_ok),
            "*reason=", order_reason,
            "*dir=", setup.direction,
            "*vol=", DoubleToString(risk.volume, 4),
            "*entry=", DoubleToString(setup.entry_price, _Digits),
            "*sl=", DoubleToString(setup.stop_price, _Digits),
            "*tp=", DoubleToString(setup.tp_price, _Digits),
            "*tpModel=", setup.tp_model,
            "*fixedRTp=", DoubleToString(setup.fixed_r_tp_price, _Digits),
            "*oppositeTouchTp=", DoubleToString(setup.opposite_touch_tp_price, _Digits),
            "*oppositeTouchNode=", setup.opposite_touch_node_id,
            "*oppositeTouchR=", DoubleToString(setup.opposite_touch_r, 4),
            "*rewardR=", DoubleToString(setup.reward_r, 4),
            "*risk=", DoubleToString(risk.estimated_total_risk_cash, 2),
            "*rawEntryEdge=", DoubleToString(setup.raw_entry_edge, _Digits),
            "*rawStopEdge=", DoubleToString(setup.raw_stop_edge, _Digits),
            "*spread=", DoubleToString(setup.spread_price, _Digits),
            "*nodeId=", setup.node_id,
            "*lastBranchSampleId=", setup.last_branch_sample_id,
            "*comment=", setup.comment
         );
      }
   }

   if(LogVerbose())
   {
      Print("DAL_E0001_CYCLE *** build=", DAL_E0001_BUILD,
         "*mode=h5_reversal_fixed_r_node_zone_ledger",
         "*setups=", setup_count,
         "*submitted=", submitted,
         "*modified=", modified,
         "*skippedExisting=", skipped_existing,
         "*skippedTouchLock=", skipped_touch_lock,
         "*skippedBlocked=", skipped_blocked,
         "*skippedRisk=", skipped_risk,
         "*skippedMarketCatch=", skipped_market_catch,
         "*skippedUpdate=", skipped_update,
         "*skippedGeometry=", skipped_geometry);
   }

   string cycle_signature = IntegerToString(setup_count) + ":" + IntegerToString(submitted) + ":" + IntegerToString(modified) + ":" + IntegerToString(skipped_existing) + ":" + IntegerToString(skipped_touch_lock) + ":" + IntegerToString(skipped_blocked) + ":" + IntegerToString(skipped_risk) + ":" + IntegerToString(skipped_market_catch) + ":" + IntegerToString(skipped_update) + ":" + IntegerToString(skipped_geometry) + ":" + g_cache_reason;
   if(LogOrders() && cycle_signature != g_last_cycle_signature)
   {
      g_last_cycle_signature = cycle_signature;
      Print("DAL_E0001_CYCLE *** build=", DAL_E0001_BUILD,
         "*mode=h5_reversal_fixed_r_node_zone_ledger",
         "*cacheReason=", g_cache_reason,
         "*setups=", setup_count,
         "*submitted=", submitted,
         "*modified=", modified,
         "*skippedExisting=", skipped_existing,
         "*skippedTouchLock=", skipped_touch_lock,
         "*skippedBlocked=", skipped_blocked,
         "*skippedRisk=", skipped_risk,
         "*skippedMarketCatch=", skipped_market_catch,
         "*skippedUpdate=", skipped_update,
         "*skippedGeometry=", skipped_geometry,
         "*tradingEnabled=", DAL_BoolToString(InpTradingEnabled));
   }

   UpdateComment("h5_r1_setups_" + IntegerToString(setup_count) + "_new_" + IntegerToString(submitted) + "_upd_" + IntegerToString(modified));
}

int OnInit()
{
   if(!SymbolSelect(LabSymbol(), true))
   {
      Print("DAL_E0001_INIT_FAIL *** reason=symbol_select_failed*symbol=", LabSymbol());
      return INIT_FAILED;
   }

   g_trade.SetExpertMagicNumber(InpMagicNumber);
   g_last_open_bar_time = 0;
   ArrayResize(g_cached_setups, 0);
   ArrayResize(g_touch_locks, 0);
   g_cache_ready = false;
   g_h5_report_refresh_counter = 0;
   g_last_h5_report_signature = "";
   g_last_outside_session_purge_bar_time = 0;

   if(LogOrders())
   {
      string session_window = E0001_FormatSessionMinute(E0001_ClampInt(InpTradingStartHour, 0, 23) * 60 + E0001_ClampInt(InpTradingStartMinute, 0, 59))
                              + "-" +
                              E0001_FormatSessionMinute(E0001_ClampInt(InpTradingEndHour, 0, 23) * 60 + E0001_ClampInt(InpTradingEndMinute, 0, 59));

      Print("DAL_E0001_BUILD_SANITY_A *** build=", DAL_E0001_BUILD,
         "*symbol=", LabSymbol(),
         "*tf=", EnumToString(LabTimeframe()),
         "*module=EXECUTION_H0005_REVERSAL_PER_CANDLE_NEAR_NODE_LIMITS",
         "*bars=", InpBars,
         "*h5Exact=PER_CANDLE_REVERSAL_NEAR_NODE_TOUCH_LIMITS",
         "*regimeBasis=", EnumToString(InpRegimeBasis),
         "*humanContext=", EnumToString(InpHumanContextSignal),
         "*htfRegimeFilter=", DAL_BoolToString(InpUseHigherTimeframeRegimeFilter),
         "*htfTf=", EnumToString(InpHigherRegimeTimeframe),
         "*useClosedBarsOnly=", DAL_BoolToString(InpUseClosedBarsOnly));

      Print("DAL_E0001_BUILD_SANITY_B *** build=", DAL_E0001_BUILD,
         "*timeFilter=", DAL_BoolToString(InpUseTradingSessionFilter),
         "*sessionClock=", EnumToString(InpTradingSessionClock),
         "*sessionWindow=", session_window,
         "*deletePendingsOutsideSession=", DAL_BoolToString(InpDeletePendingsOutsideTradingSession),
         "*h5Report=", DAL_BoolToString(InpH5ReportEnabled),
         "*h5ReportEveryNClosedBars=", InpH5ReportEveryNClosedBars,
         "*h5ReportMaxSamples=", InpH5ReportMaxSamples,
         "*h5ReportMaxBarsAfterEntry=", InpH5ReportMaxBarsAfterEntry,
         "*rewardR=", DoubleToString(InpRewardR, 4),
         "*useFixedRExitIfCloser=", DAL_BoolToString(InpUseFixedRExitIfCloser),
         "*allowOppositeTouchBelowRewardR=", DAL_BoolToString(InpAllowOppositeTouchBelowRewardR));

      Print("DAL_E0001_BUILD_SANITY_C *** build=", DAL_E0001_BUILD,
         "*entryModel=per_candle_nearest_low_buy_and_high_sell_touch_limits",
         "*researchEntryModel=touch_bar_close_in_M0005_report",
         "*stopModel=far_zone_edge_spread_adjusted_for_sell",
         "*maxSimultaneousTrades=", InpMaxSimultaneousTrades,
         "*buySlots=", InpBuyLimitSlots, "(0=unlimited)",
         "*sellSlots=", InpSellLimitSlots, "(0=unlimited)",
         "*allowOpposite=", DAL_BoolToString(InpAllowOppositeTrades),
         "*orderCommentPrefix=", E0001_ManagedCommentPrefix());

      Print("DAL_E0001_BUILD_SANITY_D *** build=", DAL_E0001_BUILD,
         "*commentIdentity=prefix_reward_direction_node",
         "*manageEveryTick=", DAL_BoolToString(InpManageOrdersEveryTick),
         "*marketCatch=", DAL_BoolToString(InpAllowMarketCatchWhenAlreadyTouching),
         "*cancelStale=", DAL_BoolToString(InpCancelStaleManagedPendings),
         "*cancelAfterEntry=", DAL_BoolToString(InpCancelManagedPendingsAfterEntry),
         "*updatePendings=", DAL_BoolToString(InpUpdateExistingManagedPendings),
         "*touchRevisitBufferPoints=", InpTouchRevisitResetBufferPoints,
         "*allowNodeRevisitRearm=", DAL_BoolToString(InpAllowNodeRevisitRearm),
         "*touchPolicy=node_locked_per_touch_unlock_only_after_full_zone_exit",
         "*tpPolicy=first_opposite_node_touch_optional_fixed_r_exit_sub_r_filter",
         "*logMode=", EnumToString(InpLogMode));
   }

   string init_session_reason = "";
   if(!E0001_IsTradingSessionOpen(init_session_reason))
   {
      E0001_ClearSetupCache("trading_session_closed_on_init*" + init_session_reason);
      string force_delete_summary = "disabled";
      int force_deleted = 0;
      if(InpDeletePendingsOutsideTradingSession)
         force_deleted = E0001_ForceDeleteManagedPendingLimits("outside_trading_session_on_init", force_delete_summary);
      if(LogOrders())
         Print("DAL_E0001_TIME_FILTER *** build=", DAL_E0001_BUILD,
            "*action=init_strict_block_all_execution_outside_session",
            "*forceDeleted=", force_deleted,
            "*deleteSummary=", force_delete_summary,
            "*", init_session_reason);
      UpdateComment("trading_session_closed");
      return INIT_SUCCEEDED;
   }

   RefreshSetupCacheIfNeeded();
   UpdateComment("initialized");
   return INIT_SUCCEEDED;
}


void OnTradeTransaction(const MqlTradeTransaction &trans, const MqlTradeRequest &request, const MqlTradeResult &result)
{
   if(trans.type != TRADE_TRANSACTION_DEAL_ADD)
      return;
   if(trans.deal == 0 || !HistoryDealSelect(trans.deal))
      return;
   if(HistoryDealGetString(trans.deal, DEAL_SYMBOL) != LabSymbol())
      return;
   if((long)HistoryDealGetInteger(trans.deal, DEAL_MAGIC) != InpMagicNumber)
      return;

   long entry_type = HistoryDealGetInteger(trans.deal, DEAL_ENTRY);
   if(entry_type != DEAL_ENTRY_IN && entry_type != DEAL_ENTRY_INOUT)
      return;

   string comment = HistoryDealGetString(trans.deal, DEAL_COMMENT);
   if(!DAL_ExecOrderCommentMatchesPrefix(comment, E0001_ManagedCommentPrefix()) && trans.order > 0)
   {
      if(HistoryOrderSelect(trans.order))
         comment = HistoryOrderGetString(trans.order, ORDER_COMMENT);
   }
   if(!DAL_ExecOrderCommentMatchesPrefix(comment, E0001_ManagedCommentPrefix()))
      return;

   int direction = 0;
   long deal_type = HistoryDealGetInteger(trans.deal, DEAL_TYPE);
   if(deal_type == DEAL_TYPE_BUY)
      direction = +1;
   else if(deal_type == DEAL_TYPE_SELL)
      direction = -1;

   double entry_price = HistoryDealGetDouble(trans.deal, DEAL_PRICE);
   DALExecReversalSetup setup;
   bool setup_found = FindSetupInCacheByComment(comment, setup);
   if(setup_found)
   {
      direction = setup.direction;
      entry_price = setup.entry_price;
      E0001_SetTouchLockFromSetup(setup);
   }
   else
   {
      E0001_SetTouchLock(comment, direction, entry_price);
   }

   if(LogOrders())
      Print("DAL_E0001_NODE_TOUCH_LOCK *** build=", DAL_E0001_BUILD, "*deal=", (long)trans.deal, "*dir=", direction, "*entry=", DoubleToString(entry_price, _Digits), "*setupFound=", DAL_BoolToString(setup_found), "*nodeId=", setup.node_id, "*comment=", comment);
}

void OnDeinit(const int reason)
{
   Comment("");
}

void OnTick()
{
   string session_reason = "";
   if(!E0001_IsTradingSessionOpen(session_reason))
   {
      E0001_ClearSetupCache("trading_session_closed*" + session_reason);

      string force_delete_summary = "disabled";
      int force_deleted = 0;
      bool ran_purge = false;
      if(InpDeletePendingsOutsideTradingSession)
      {
         if(E0001_ShouldRunOutsideSessionPurge())
         {
            ran_purge = true;
            force_deleted = E0001_ForceDeleteManagedPendingLimits("outside_trading_session", force_delete_summary);
         }
         else
            force_delete_summary = "throttled_until_next_bar";
      }

      string signature = session_reason + "*purge=" + DAL_BoolToString(ran_purge) + "*forceDeleted=" + IntegerToString(force_deleted) + "*" + force_delete_summary;
      if(LogOrders() && g_last_cycle_signature != signature)
      {
         g_last_cycle_signature = signature;
         Print("DAL_E0001_TIME_FILTER *** build=", DAL_E0001_BUILD,
            "*action=strict_block_all_execution_outside_session",
            "*deletePendings=", DAL_BoolToString(InpDeletePendingsOutsideTradingSession),
            "*purgeRun=", DAL_BoolToString(ran_purge),
            "*forceDeleted=", force_deleted,
            "*deleteSummary=", force_delete_summary,
            "*", session_reason);
      }
      UpdateComment("trading_session_closed");
      return;
   }

   bool refreshed = RefreshSetupCacheIfNeeded();

   if(!InpManageOrdersEveryTick && !refreshed)
      return;

   TryPlaceCachedSetups();
}
