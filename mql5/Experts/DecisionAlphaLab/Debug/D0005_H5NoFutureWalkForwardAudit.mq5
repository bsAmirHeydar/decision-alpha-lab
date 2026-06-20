//+------------------------------------------------------------------+
//| Decision Alpha Lab — D0005 H5 No-Future Walk-Forward Audit        |
//| Replays H0005/M0001/M0002 candle by candle using prefix-only data |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property description "Debug EA for H0005 no-future validation: walk-forward, prefix-only, candle-by-candle audit."

#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/M0002/DAL_M0002Engine.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecReversalOneToOne.mqh>

#define DAL_D0005_BUILD "1.00"

input string InpSymbol = "";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpReplayClosedBars = 1500;
input int InpWarmupClosedBars = 250;

// Shared H5/M0001 structure.
input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;

// M0002 regime settings.
input int InpRegimeLookbackBars = 100;
input int InpOutcomeCandleOffsetAfterExit = 0;
input int InpBrokerUtcOffsetHours = 0;

// Audit controls.
input bool InpRunHistoricalWalkForwardOnInit = true;
input bool InpProbeLiveOnNewClosedBar = true;
input int InpPrintEveryNSteps = 100;
input bool InpPrintOnlyOnRegimeChange = false;
input bool InpWriteCsv = true;
input string InpCsvFileName = "D0005_H5_NoFuture_WalkForward.csv";

struct D0005AuditStep
{
   datetime cursor_time;
   int bars_count;
   int nodes_count;
   int active_nodes_count;
   int future_node_violations;
   int events_count;
   bool has_last_sample;
   ENUM_DALM0002Outcome last_outcome;
   int last_event_index;
   bool pass_no_future;
   string reason;
};

datetime g_last_open_bar_time = 0;
int g_csv_handle = INVALID_HANDLE;
ENUM_DALM0002Outcome g_last_printed_outcome = DAL_M0002_OUTCOME_NONE;
bool g_last_printed_has_sample = false;

string D0005_Symbol()
{
   if(InpSymbol == "")
      return _Symbol;
   return InpSymbol;
}

ENUM_TIMEFRAMES D0005_Timeframe()
{
   if(InpTimeframe == PERIOD_CURRENT)
      return (ENUM_TIMEFRAMES)_Period;
   return InpTimeframe;
}

string D0005_TwoDigits(const int value)
{
   if(value < 10)
      return "0" + IntegerToString(value);
   return IntegerToString(value);
}

string D0005_FormatDateTime(const datetime value)
{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d.%02d.%02d %02d:%02d:%02d", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
}

string D0005_BoolToString(const bool value)
{
   return (value ? "true" : "false");
}

string D0005_RegimeOutcomeToString(const ENUM_DALM0002Outcome outcome)
{
   if(outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT)
      return "REVERSAL_AFTER_EXIT";
   if(outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT)
      return "CONTINUATION_AFTER_EXIT";
   if(outcome == DAL_M0002_OUTCOME_NONE)
      return "NONE";
   return EnumToString(outcome);
}

void D0005_BuildM0001Config(DALM0001Config &config)
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

void D0005_BuildM0002Config(DALM0002Config &config)
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

bool D0005_HasNewOpenCandle()
{
   datetime current_open = iTime(D0005_Symbol(), D0005_Timeframe(), 0);
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

void D0005_ReverseRates(MqlRates &rates[], const int count)
{
   int left = 0;
   int right = count - 1;
   while(left < right)
   {
      MqlRates tmp = rates[left];
      rates[left] = rates[right];
      rates[right] = tmp;
      left++;
      right--;
   }
}

// Critical no-future loader: every audit step requests only the prefix ending
// at simulated_cursor_closed_shift. It never copies the full history unless the
// caller explicitly asks another function to do so.
bool D0005_LoadPrefixBarsByClosedShift(
   const int oldest_closed_shift,
   const int simulated_cursor_closed_shift,
   DALBar &bars[],
   int &bars_count,
   string &reason
)
{
   ArrayResize(bars, 0);
   bars_count = 0;
   reason = "not_loaded";

   if(oldest_closed_shift < simulated_cursor_closed_shift)
   {
      reason = "bad_shift_order";
      return false;
   }

   datetime start_time = iTime(D0005_Symbol(), D0005_Timeframe(), oldest_closed_shift);
   datetime stop_time = iTime(D0005_Symbol(), D0005_Timeframe(), simulated_cursor_closed_shift);
   if(start_time <= 0 || stop_time <= 0)
   {
      reason = "bad_iTime*oldestShift=" + IntegerToString(oldest_closed_shift)
         + "*cursorShift=" + IntegerToString(simulated_cursor_closed_shift);
      return false;
   }

   if(start_time > stop_time)
   {
      datetime tmp_time = start_time;
      start_time = stop_time;
      stop_time = tmp_time;
   }

   MqlRates raw[];
   ArrayResize(raw, 0);
   int copied = CopyRates(D0005_Symbol(), D0005_Timeframe(), start_time, stop_time, raw);
   if(copied <= 0)
   {
      reason = "copy_rates_failed*err=" + IntegerToString(GetLastError())
         + "*start=" + D0005_FormatDateTime(start_time)
         + "*stop=" + D0005_FormatDateTime(stop_time);
      return false;
   }

   if(copied > 1 && raw[0].time > raw[copied - 1].time)
      D0005_ReverseRates(raw, copied);

   ArrayResize(bars, copied);
   for(int i = 0; i < copied; i++)
   {
      ZeroMemory(bars[i]);
      bars[i].time = raw[i].time;
      bars[i].open = raw[i].open;
      bars[i].high = raw[i].high;
      bars[i].low = raw[i].low;
      bars[i].close = raw[i].close;
   }

   bars_count = copied;
   reason = "loaded_prefix_only*start=" + D0005_FormatDateTime(raw[0].time)
      + "*stop=" + D0005_FormatDateTime(raw[copied - 1].time)
      + "*bars=" + IntegerToString(copied);
   return true;
}

bool D0005_EvaluatePrefix(const DALBar &bars[], const int bars_count, D0005AuditStep &step)
{
   step.cursor_time = (bars_count > 0 ? bars[bars_count - 1].time : 0);
   step.bars_count = bars_count;
   step.last_outcome = DAL_M0002_OUTCOME_NONE;
   step.last_event_index = -1;
   step.pass_no_future = false;
   step.reason = "not_evaluated";

   if(bars_count <= InpL * 2 + 10)
   {
      step.reason = "not_enough_bars";
      return false;
   }

   DALM0001Config m1;
   D0005_BuildM0001Config(m1);

   DALLRuleNode nodes[];
   int nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, m1.L, nodes);
   step.nodes_count = nodes_count;

   int last_bar_index = bars_count - 1;
   int future_nodes = 0;
   int active_nodes = 0;
   for(int i = 0; i < nodes_count; i++)
   {
      if(!nodes[i].confirmed)
         continue;

      if(nodes[i].active_from_index > last_bar_index)
      {
         future_nodes++;
         continue;
      }

      if(nodes[i].active_from_index >= 0)
         active_nodes++;
   }
   step.active_nodes_count = active_nodes;
   step.future_node_violations = future_nodes;

   DALM0001Event events[];
   int events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, m1, events);
   step.events_count = events_count;

   DALM0002Config m2;
   D0005_BuildM0002Config(m2);

   DALM0002BranchSample last_sample;
   int last_event_index = -1;
   bool has_last_sample = DAL_ExecFindLatestBranchSampleFast(events, events_count, bars, bars_count, 0, m2, last_sample, last_event_index);

   step.has_last_sample = has_last_sample;
   step.last_event_index = last_event_index;
   if(has_last_sample)
      step.last_outcome = last_sample.outcome;

   step.pass_no_future = (future_nodes == 0);
   step.reason = "prefix_eval_ok";
   if(!has_last_sample)
      step.reason = "prefix_eval_ok*no_last_branch";
   if(future_nodes > 0)
      step.reason = "future_node_violation";

   return true;
}

void D0005_OpenCsvIfNeeded()
{
   if(!InpWriteCsv)
      return;
   if(g_csv_handle != INVALID_HANDLE)
      return;

   g_csv_handle = FileOpen(InpCsvFileName, FILE_WRITE | FILE_CSV | FILE_ANSI);
   if(g_csv_handle == INVALID_HANDLE)
   {
      Print("DAL_D0005_CSV_OPEN_FAILED *** build=", DAL_D0005_BUILD,
         "*file=", InpCsvFileName,
         "*err=", GetLastError());
      return;
   }

   FileWrite(g_csv_handle,
      "cursor_time",
      "bars_count",
      "nodes_count",
      "active_nodes_count",
      "future_node_violations",
      "events_count",
      "has_last_sample",
      "last_outcome",
      "last_event_index",
      "pass_no_future",
      "reason");
}

void D0005_WriteCsvStep(const D0005AuditStep &step)
{
   if(!InpWriteCsv)
      return;
   D0005_OpenCsvIfNeeded();
   if(g_csv_handle == INVALID_HANDLE)
      return;

   FileWrite(g_csv_handle,
      D0005_FormatDateTime(step.cursor_time),
      step.bars_count,
      step.nodes_count,
      step.active_nodes_count,
      step.future_node_violations,
      step.events_count,
      D0005_BoolToString(step.has_last_sample),
      D0005_RegimeOutcomeToString(step.last_outcome),
      step.last_event_index,
      D0005_BoolToString(step.pass_no_future),
      step.reason);
}

bool D0005_ShouldPrintStep(const int step_number, const D0005AuditStep &step)
{
   if(InpPrintOnlyOnRegimeChange)
   {
      bool changed = (step.has_last_sample != g_last_printed_has_sample || step.last_outcome != g_last_printed_outcome);
      if(changed)
      {
         g_last_printed_has_sample = step.has_last_sample;
         g_last_printed_outcome = step.last_outcome;
      }
      return changed;
   }

   int every_n = MathMax(1, InpPrintEveryNSteps);
   if((step_number % every_n) == 0)
      return true;

   if(!step.pass_no_future)
      return true;

   return false;
}

void D0005_PrintStep(const string tag, const int step_number, const D0005AuditStep &step)
{
   Print(tag, " *** build=", DAL_D0005_BUILD,
      "*step=", step_number,
      "*cursor=", D0005_FormatDateTime(step.cursor_time),
      "*bars=", step.bars_count,
      "*nodes=", step.nodes_count,
      "*activeNodes=", step.active_nodes_count,
      "*futureNodeViolations=", step.future_node_violations,
      "*events=", step.events_count,
      "*hasLast=", D0005_BoolToString(step.has_last_sample),
      "*last=", D0005_RegimeOutcomeToString(step.last_outcome),
      "*lastEventIndex=", step.last_event_index,
      "*passNoFuture=", D0005_BoolToString(step.pass_no_future),
      "*reason=", step.reason);
}

bool D0005_RunHistoricalWalkForwardAudit()
{
   int total_bars = Bars(D0005_Symbol(), D0005_Timeframe());
   if(total_bars <= 0)
   {
      Print("DAL_D0005_AUDIT_FAILED *** build=", DAL_D0005_BUILD,
         "*reason=no_bars*symbol=", D0005_Symbol(),
         "*tf=", EnumToString(D0005_Timeframe()));
      return false;
   }

   int replay_closed = MathMax(50, InpReplayClosedBars);
   int max_oldest_shift = MathMin(total_bars - 1, replay_closed);
   int warmup = MathMax(InpWarmupClosedBars, InpL * 2 + 20);
   if(max_oldest_shift <= warmup)
   {
      Print("DAL_D0005_AUDIT_FAILED *** build=", DAL_D0005_BUILD,
         "*reason=not_enough_replay_bars",
         "*totalBars=", total_bars,
         "*maxOldestShift=", max_oldest_shift,
         "*warmup=", warmup);
      return false;
   }

   D0005_OpenCsvIfNeeded();

   int steps = 0;
   int ok_steps = 0;
   int failed_steps = 0;
   int future_violation_steps = 0;
   int no_branch_steps = 0;
   int reversal_steps = 0;
   int continuation_steps = 0;
   int regime_changes = 0;
   bool prev_has = false;
   ENUM_DALM0002Outcome prev_outcome = DAL_M0002_OUTCOME_NONE;

   Print("DAL_D0005_AUDIT_START *** build=", DAL_D0005_BUILD,
      "*mode=historical_walk_forward_prefix_only",
      "*symbol=", D0005_Symbol(),
      "*tf=", EnumToString(D0005_Timeframe()),
      "*totalBars=", total_bars,
      "*oldestClosedShift=", max_oldest_shift,
      "*warmupClosedBars=", warmup,
      "*contract=one_CopyRates_prefix_per_step_no_full_history_decision");

   // Closed shift decreases from old history toward the latest closed bar.
   // Each cursor gets its own prefix copy, bounded by cursor time.
   for(int cursor_shift = max_oldest_shift - warmup; cursor_shift >= 1; cursor_shift--)
   {
      steps++;
      int oldest_shift_for_step = max_oldest_shift;
      DALBar bars[];
      int bars_count = 0;
      string load_reason = "";
      bool loaded = D0005_LoadPrefixBarsByClosedShift(oldest_shift_for_step, cursor_shift, bars, bars_count, load_reason);
      if(!loaded)
      {
         failed_steps++;
         if((steps % MathMax(1, InpPrintEveryNSteps)) == 0)
         {
            Print("DAL_D0005_STEP_LOAD_FAILED *** build=", DAL_D0005_BUILD,
               "*step=", steps,
               "*cursorShift=", cursor_shift,
               "*reason=", load_reason);
         }
         continue;
      }

      D0005AuditStep step;
      bool evaluated = D0005_EvaluatePrefix(bars, bars_count, step);
      if(!evaluated)
         failed_steps++;
      else
         ok_steps++;

      if(step.future_node_violations > 0)
         future_violation_steps++;
      if(!step.has_last_sample)
         no_branch_steps++;
      else if(step.last_outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT)
         reversal_steps++;
      else if(step.last_outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT)
         continuation_steps++;

      if(steps > 1 && step.has_last_sample && prev_has && step.last_outcome != prev_outcome)
         regime_changes++;
      if(step.has_last_sample)
      {
         prev_has = true;
         prev_outcome = step.last_outcome;
      }

      D0005_WriteCsvStep(step);
      if(D0005_ShouldPrintStep(steps, step))
         D0005_PrintStep("DAL_D0005_WF_STEP", steps, step);
   }

   if(g_csv_handle != INVALID_HANDLE)
      FileFlush(g_csv_handle);

   bool pass = (future_violation_steps == 0 && ok_steps > 0);
   Print("DAL_D0005_AUDIT_SUMMARY *** build=", DAL_D0005_BUILD,
      "*pass=", D0005_BoolToString(pass),
      "*steps=", steps,
      "*okSteps=", ok_steps,
      "*failedSteps=", failed_steps,
      "*futureViolationSteps=", future_violation_steps,
      "*noBranchSteps=", no_branch_steps,
      "*reversalSteps=", reversal_steps,
      "*continuationSteps=", continuation_steps,
      "*regimeChanges=", regime_changes,
      "*csv=", (InpWriteCsv ? InpCsvFileName : "OFF"));

   return pass;
}

void D0005_RunLiveClosedBarProbe()
{
   if(!InpProbeLiveOnNewClosedBar)
      return;

   int total_bars = Bars(D0005_Symbol(), D0005_Timeframe());
   if(total_bars <= 0)
      return;

   int lookback = MathMax(InpWarmupClosedBars + InpRegimeLookbackBars + InpL * 4 + 50, 300);
   int oldest_shift = MathMin(total_bars - 1, lookback);
   if(oldest_shift <= 2)
      return;

   DALBar bars[];
   int bars_count = 0;
   string load_reason = "";
   if(!D0005_LoadPrefixBarsByClosedShift(oldest_shift, 1, bars, bars_count, load_reason))
   {
      Print("DAL_D0005_LIVE_PROBE_LOAD_FAILED *** build=", DAL_D0005_BUILD,
         "*reason=", load_reason);
      return;
   }

   D0005AuditStep step;
   D0005_EvaluatePrefix(bars, bars_count, step);
   D0005_WriteCsvStep(step);
   D0005_PrintStep("DAL_D0005_LIVE_STEP", 0, step);
}

int OnInit()
{
   Print("DAL_D0005_INIT *** build=", DAL_D0005_BUILD,
      "*purpose=H0005_no_future_walk_forward_audit",
      "*symbol=", D0005_Symbol(),
      "*tf=", EnumToString(D0005_Timeframe()),
      "*runHistorical=", D0005_BoolToString(InpRunHistoricalWalkForwardOnInit),
      "*liveProbe=", D0005_BoolToString(InpProbeLiveOnNewClosedBar));

   if(InpRunHistoricalWalkForwardOnInit)
      D0005_RunHistoricalWalkForwardAudit();

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   if(g_csv_handle != INVALID_HANDLE)
   {
      FileClose(g_csv_handle);
      g_csv_handle = INVALID_HANDLE;
   }

   Print("DAL_D0005_DEINIT *** build=", DAL_D0005_BUILD,
      "*reason=", reason);
}

void OnTick()
{
   if(!D0005_HasNewOpenCandle())
      return;

   D0005_RunLiveClosedBarProbe();
}
