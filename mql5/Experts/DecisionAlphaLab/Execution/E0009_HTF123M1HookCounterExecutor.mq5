//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0009 HTF 123 M1 Hook Counter Executor       |
//| Simple model: 3 HTF highs/lows -> counter entries on M1 hooks     |
//+------------------------------------------------------------------+
#property strict
#property version   "1.08"
#property description "E0009: HTF 3-swing counter entries on unique M1 micro hooks with persistent hook ledger."

#include <Trade/Trade.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/Execution/E0009/DAL_E0009Modules.mqh>

input string InpSymbol = "";
input ENUM_TIMEFRAMES InpHTFTimeframe = PERIOD_M15;
input ENUM_TIMEFRAMES InpExecutionTF = PERIOD_M1;

input int InpHTFBars = 1000;
input int InpM1Bars = 500;

input int InpHTFL = 2;
input int InpM1L = 2;
input double InpZoneRatio = 0.90;

input int InpHTF123MaxAgeBars = 0;  // 0 = no HTF 123 age limit
input int InpM1HookMaxAgeBars = 40;
input bool InpRequireFreshM1HookAfterHTF123Close = true;
input bool InpRejectHuntedM1Hook = false;
input int InpMaxHookCandidatesPerBar = 3;
input bool InpOneTradePerHookForever = true; // persistent in-memory hook ledger for the whole test/session

// Micro-only filter: reject large M1 hook extremes.
input bool InpUseMicroOnlyFilter = true;
input double InpMaxHookRiskToHTFAmplitude = 0.08; // 8% of HTF 123 amplitude
input int InpMicroAvgRangeBars = 80;
input double InpMaxHookRiskToM1AvgRange = 3.0;    // 3x recent M1 average range
input int InpMaxHookRiskPoints = 0;               // 0 = disabled

input ENUM_DAL_E0009_COUNTER_MODE InpCounterMode = DAL_E0009_COUNTER_OPPOSITE_123;
input ENUM_DAL_E0009_ORDER_MODE InpOrderMode = DAL_E0009_ORDER_MARKET_ON_CONFIRM;
input ENUM_DAL_E0009_EXIT_MODE InpExitMode = DAL_E0009_EXIT_HTF_THIRD_OPPOSITE_SWING;
input double InpFixedR = 50.0;
input int InpHTFTpSwingCount = 3;

input double InpBuyEntrySpreadMultiplier = 1.0;
input double InpSellStopSpreadMultiplier = 1.0;

input long InpMagicNumber = 9009009;
input string InpOrderCommentPrefix = "DALE9";
input double InpRiskCash = 100.0;
input bool InpAllowMinLotIfRiskTooSmall = false;
input double InpCommissionPerLotRoundTurn = 0.0;
input int InpMaxPendingPerSide = 0;
input int InpMaxPositionsPerSide = 0;

input bool InpTradingEnabled = true;
input bool InpRunOnInit = true;
input int InpUpdateEveryNM1Bars = 1;
input bool InpPrintLogs = true;
input bool InpPrintRejectLogs = true;

#define DAL_E0009_BUILD "1.08"

CTrade g_trade;
datetime g_last_execution_open_time = 0;
datetime g_last_htf_open_time = 0;
int g_m1_bar_counter = 0;

DALE0009HTF123State g_htf123_cache;
bool g_htf123_evaluated = false;

DALLRuleNode g_htf_nodes_cache[];
int g_htf_nodes_count_cache = 0;

string g_used_hook_keys[];
int g_used_hook_keys_count = 0;

string E0009_Symbol()
{
   return (InpSymbol == "" ? _Symbol : InpSymbol);
}

bool E0009_HookKeyUsed(const string key)
{
   if(key == "")
      return false;

   for(int i = 0; i < g_used_hook_keys_count; i++)
   {
      if(g_used_hook_keys[i] == key)
         return true;
   }

   return false;
}

void E0009_MarkHookKeyUsed(const string key)
{
   if(key == "")
      return;

   if(E0009_HookKeyUsed(key))
      return;

   int n = g_used_hook_keys_count;
   ArrayResize(g_used_hook_keys, n + 1);
   g_used_hook_keys[n] = key;
   g_used_hook_keys_count = n + 1;
}

DALE0009Config E0009_Config()
{
   DALE0009Config c;
   c.htf_L = MathMax(1, InpHTFL);
   c.m1_L = MathMax(1, InpM1L);
   c.zone_ratio = MathMax(0.0, MathMin(0.9999, InpZoneRatio));
   c.htf_max_age_bars = MathMax(0, InpHTF123MaxAgeBars);
   c.m1_max_hook_age_bars = MathMax(0, InpM1HookMaxAgeBars);
   c.fixed_r = MathMax(0.0, InpFixedR);
   c.htf_tp_swing_count = MathMax(1, InpHTFTpSwingCount);
   c.require_fresh_m1_hook_after_htf_close = InpRequireFreshM1HookAfterHTF123Close;
   c.reject_hunted_m1_hook = InpRejectHuntedM1Hook;
   c.max_hook_candidates_per_bar = MathMax(1, InpMaxHookCandidatesPerBar);

   c.use_micro_only_filter = InpUseMicroOnlyFilter;
   c.max_hook_risk_to_htf_amplitude = MathMax(0.0, InpMaxHookRiskToHTFAmplitude);
   c.micro_avg_range_bars = MathMax(0, InpMicroAvgRangeBars);
   c.max_hook_risk_to_m1_avg_range = MathMax(0.0, InpMaxHookRiskToM1AvgRange);
   c.max_hook_risk_points = MathMax(0, InpMaxHookRiskPoints);

   c.buy_entry_spread_mult = MathMax(0.0, InpBuyEntrySpreadMultiplier);
   c.sell_stop_spread_mult = MathMax(0.0, InpSellStopSpreadMultiplier);
   c.counter_mode = InpCounterMode;
   c.exit_mode = InpExitMode;
   c.order_mode = InpOrderMode;
   return c;
}

bool E0009_UpdateHTF123Cache(const string symbol, const DALE0009Config &cfg, const bool force)
{
   datetime htf_open = iTime(symbol, InpHTFTimeframe, 0);
   if(htf_open <= 0)
      return false;

   bool refresh = force || !g_htf123_evaluated || htf_open != g_last_htf_open_time;
   if(!refresh)
      return g_htf123_cache.valid;

   g_last_htf_open_time = htf_open;
   g_htf123_evaluated = true;

   DALBar htf_bars[];
   DALLRuleNode htf_nodes[];
   int bars_count = 0, nodes_count = 0;
   string reason = "";

   if(!DAL_E0009LoadNodes(symbol, InpHTFTimeframe, MathMax(200, InpHTFBars), cfg.htf_L, htf_bars, bars_count, htf_nodes, nodes_count, reason))
   {
      ArrayResize(g_htf_nodes_cache, 0);
      g_htf_nodes_count_cache = 0;
      DAL_E0009_Reset123(g_htf123_cache);
      g_htf123_cache.tf = InpHTFTimeframe;
      g_htf123_cache.reason = reason;
      return false;
   }

   ArrayResize(g_htf_nodes_cache, nodes_count);
   for(int k = 0; k < nodes_count; k++)
      g_htf_nodes_cache[k] = htf_nodes[k];
   g_htf_nodes_count_cache = nodes_count;

   if(!DAL_E0009FindLatestClosed123(htf_nodes, nodes_count, bars_count, InpHTFTimeframe, cfg.htf_max_age_bars, g_htf123_cache))
      return false;

   return true;
}

void E0009_Process(const string run_mode)
{
   string symbol = E0009_Symbol();
   DALE0009Config cfg = E0009_Config();
   DALE0009Diagnostics diag;
   DAL_E0009_ResetDiagnostics(diag);

   bool htf_ok = E0009_UpdateHTF123Cache(symbol, cfg, run_mode == "INIT");

   int tp_checked = 0, tp_modified = 0, tp_waiting = 0, tp_rejected = 0;
   if(cfg.exit_mode == DAL_E0009_EXIT_HTF_THIRD_OPPOSITE_SWING && g_htf_nodes_count_cache > 0)
      DAL_E0009SyncHTFThirdSwingTP(symbol, InpMagicNumber, InpOrderCommentPrefix,
                                   g_htf_nodes_cache, g_htf_nodes_count_cache,
                                   cfg.htf_tp_swing_count, g_trade,
                                   tp_checked, tp_modified, tp_waiting, tp_rejected);

   if(!htf_ok || !g_htf123_cache.valid)
   {
      diag.htf_missing++;
      if(InpPrintLogs && InpPrintRejectLogs)
         Print("DAL_E0009_SKIP *** build=", DAL_E0009_BUILD,
            "*runMode=", run_mode,
            "*reason=no_closed_htf_123",
            "*detail=", g_htf123_cache.reason);
      return;
   }
   diag.htf_ok++;

   DALBar m1_bars[];
   DALLRuleNode m1_nodes[];
   int m1_bars_count = 0, m1_nodes_count = 0;
   string reason = "";

   if(!DAL_E0009LoadNodes(symbol, InpExecutionTF, MathMax(200, InpM1Bars), cfg.m1_L, m1_bars, m1_bars_count, m1_nodes, m1_nodes_count, reason))
   {
      diag.m1_map_failed++;
      if(InpPrintLogs && InpPrintRejectLogs)
         Print("DAL_E0009_SKIP *** build=", DAL_E0009_BUILD, "*runMode=", run_mode, "*reason=m1_map_failed_", reason);
      return;
   }
   diag.m1_map_ok++;

   int directions[2];
   int dir_count = 1;
   directions[0] = DAL_E0009TradeDirectionFrom123(g_htf123_cache, cfg.counter_mode);

   if(cfg.counter_mode == DAL_E0009_COUNTER_BOTH_FOR_TEST)
   {
      dir_count = 2;
      directions[0] = +1;
      directions[1] = -1;
   }

   int planned = 0;
   int sent = 0;
   int rejected = 0;

   for(int i = 0; i < dir_count; i++)
   {
      int trade_direction = directions[i];

      DALE0009HookSignal signals[];
      int signals_count = DAL_E0009CollectHookSignals(symbol, m1_bars, m1_bars_count, m1_nodes, m1_nodes_count,
                                                       g_htf123_cache, trade_direction, cfg, signals, diag);

      if(signals_count <= 0)
      {
         rejected++;
         if(InpPrintLogs && InpPrintRejectLogs)
            Print("DAL_E0009_HOOK_REJECT *** build=", DAL_E0009_BUILD,
               "*dir=", trade_direction,
               "*reason=no_valid_hook_signal",
               "*htf123=", DAL_E0009DirectionName(g_htf123_cache.direction),
               "*seen=", diag.hook_seen,
               "*afterTimeReject=", diag.hook_after_time_reject,
               "*ageReject=", diag.hook_age_reject,
               "*zoneFail=", diag.hook_zone_failed,
               "*huntedReject=", diag.hook_hunted_reject,
               "*microReject=", diag.hook_micro_reject);
         continue;
      }

      for(int s = 0; s < signals_count; s++)
      {
         DALE0009HookSignal sig = signals[s];

         if(InpOneTradePerHookForever && E0009_HookKeyUsed(sig.comment))
         {
            diag.duplicate_skip++;
            if(InpPrintLogs && InpPrintRejectLogs)
               Print("DAL_E0009_HOOK_DUPLICATE_SKIP *** build=", DAL_E0009_BUILD,
                  "*reason=hook_key_already_used",
                  "*comment=", sig.comment);
            continue;
         }

         planned++;
         diag.planned++;

         string send_reason = "plan_only";
         bool ok = true;
         if(InpTradingEnabled)
            ok = DAL_E0009SendHookOrder(symbol, InpMagicNumber, InpOrderCommentPrefix,
                                        InpRiskCash, InpCommissionPerLotRoundTurn,
                                        InpAllowMinLotIfRiskTooSmall,
                                        InpMaxPendingPerSide, InpMaxPositionsPerSide,
                                        sig, g_trade, send_reason, diag);

         if(ok)
         {
            sent++;
            diag.sent_or_plan++;

            if(InpOneTradePerHookForever)
               E0009_MarkHookKeyUsed(sig.comment);

            if(InpPrintLogs)
               Print("DAL_E0009_PLAN *** build=", DAL_E0009_BUILD,
                  "*runMode=", run_mode,
                  "*htfTF=", EnumToString(InpHTFTimeframe),
                  "*htf123=", DAL_E0009DirectionName(g_htf123_cache.direction),
                  "*p1=", DoubleToString(g_htf123_cache.p1.price, _Digits),
                  "*p2=", DoubleToString(g_htf123_cache.p2.price, _Digits),
                  "*p3=", DoubleToString(g_htf123_cache.p3.price, _Digits),
                  "*tradeDir=", sig.direction,
                  "*hookNode=", sig.hook_node.id,
                  "*hookType=", (sig.hook_node.type == DAL_NODE_LOW ? "LOW" : "HIGH"),
                  "*orderMode=", DAL_E0009OrderModeName(sig.order_mode),
                  "*orderKind=", DAL_E0009OrderKindName(sig.order_kind),
                  "*entry=", DoubleToString(sig.entry, _Digits),
                  "*sl=", DoubleToString(sig.sl, _Digits),
                  "*tp=", DoubleToString(sig.tp, _Digits),
                  "*risk=", DoubleToString(sig.risk_distance, _Digits),
                  "*R=", DoubleToString(sig.potential_r, 2),
                  "*comment=", sig.comment,
                  "*send=", send_reason);
         }
         else
         {
            rejected++;
            if(InpPrintLogs && InpPrintRejectLogs)
               Print("DAL_E0009_SEND_REJECT *** build=", DAL_E0009_BUILD,
                  "*reason=", send_reason,
                  "*comment=", sig.comment,
                  "*orderKind=", DAL_E0009OrderKindName(sig.order_kind));
         }
      }
   }

   if(InpPrintLogs)
   {
      Print("DAL_E0009_AUDIT_A *** build=", DAL_E0009_BUILD,
         "*runMode=", run_mode,
         "*symbol=", symbol,
         "*htf=", EnumToString(InpHTFTimeframe),
         "*execTF=", EnumToString(InpExecutionTF),
         "*Lhtf=", cfg.htf_L,
         "*Lm1=", cfg.m1_L,
         "*htf123=", DAL_E0009DirectionName(g_htf123_cache.direction),
         "*htfAge=", g_htf123_cache.age_bars,
         "*closedTime=", TimeToString(g_htf123_cache.closed_time),
         "*orderMode=", DAL_E0009OrderModeName(cfg.order_mode),
         "*exitMode=", DAL_E0009ExitModeName(cfg.exit_mode));

      Print("DAL_E0009_AUDIT_B *** build=", DAL_E0009_BUILD,
         "*fixedR=", DoubleToString(cfg.fixed_r, 2),
         "*htfTpSwingCount=", cfg.htf_tp_swing_count,
         "*hookSeen=", diag.hook_seen,
         "*hookAfterTimeReject=", diag.hook_after_time_reject,
         "*hookAgeReject=", diag.hook_age_reject,
         "*hookZoneFail=", diag.hook_zone_failed,
         "*hookHuntedReject=", diag.hook_hunted_reject,
         "*hookMicroReject=", diag.hook_micro_reject,
         "*hookBuilt=", diag.hook_built,
         "*microFilter=", DAL_BoolToString(cfg.use_micro_only_filter),
         "*maxRiskToHTF=", DoubleToString(cfg.max_hook_risk_to_htf_amplitude, 4),
         "*maxRiskToM1Avg=", DoubleToString(cfg.max_hook_risk_to_m1_avg_range, 2),
         "*maxRiskPoints=", cfg.max_hook_risk_points);

      Print("DAL_E0009_AUDIT_C *** build=", DAL_E0009_BUILD,
         "*geometryReject=", diag.geometry_reject,
         "*riskReject=", diag.risk_reject,
         "*capReject=", diag.cap_reject,
         "*duplicateSkip=", diag.duplicate_skip,
         "*usedHookKeys=", g_used_hook_keys_count,
         "*oneTradePerHook=", DAL_BoolToString(InpOneTradePerHookForever),
         "*tpChecked=", tp_checked,
         "*tpModified=", tp_modified,
         "*tpWaiting=", tp_waiting,
         "*tpRejected=", tp_rejected,
         "*planned=", planned,
         "*sentOrPlan=", sent,
         "*rejected=", rejected);
   }
}

int OnInit()
{
   g_trade.SetExpertMagicNumber(InpMagicNumber);

   DAL_E0009_Reset123(g_htf123_cache);
   g_htf123_evaluated = false;
   ArrayResize(g_htf_nodes_cache, 0);
   g_htf_nodes_count_cache = 0;
   ArrayResize(g_used_hook_keys, 0);
   g_used_hook_keys_count = 0;

   Print("DAL_E0009_BUILD_SANITY *** build=", DAL_E0009_BUILD,
      "*module=HTF_THREE_SWINGS_M1_HOOK_COUNTER",
      "*htf=", EnumToString(InpHTFTimeframe),
      "*execTF=", EnumToString(InpExecutionTF),
      "*counterMode=", (InpCounterMode == DAL_E0009_COUNTER_OPPOSITE_123 ? "OPPOSITE_123" : "BOTH_FOR_TEST"),
      "*orderMode=", DAL_E0009OrderModeName(InpOrderMode),
      "*exitMode=", DAL_E0009ExitModeName(InpExitMode),
      "*microFilter=", DAL_BoolToString(InpUseMicroOnlyFilter),
      "*oneTradePerHook=", DAL_BoolToString(InpOneTradePerHookForever),
      "*maxRiskToHTF=", DoubleToString(InpMaxHookRiskToHTFAmplitude, 4),
      "*maxRiskToM1Avg=", DoubleToString(InpMaxHookRiskToM1AvgRange, 2),
      "*tradingEnabled=", DAL_BoolToString(InpTradingEnabled));

   if(InpRunOnInit)
      E0009_Process("INIT");

   return INIT_SUCCEEDED;
}

void OnTick()
{
   string symbol = E0009_Symbol();
   datetime open_time = iTime(symbol, InpExecutionTF, 0);
   if(open_time <= 0)
      return;

   if(open_time == g_last_execution_open_time)
      return;

   g_last_execution_open_time = open_time;
   g_m1_bar_counter++;

   int every = MathMax(1, InpUpdateEveryNM1Bars);
   if((g_m1_bar_counter % every) != 0)
      return;

   E0009_Process("NEW_EXECUTION_BAR");
}
