//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0009 Multi-Level 123 Hook Executor          |
//| Macro H4 mode + M15 setup + M1 hooks + H4 monotonic exit          |
//+------------------------------------------------------------------+
#property strict
#property version   "1.12"
#property description "E0009: reversal macro scan, latest-only setup, limit-touch hook entry, and structural exit TP."

#include <Trade/Trade.mqh>
#include <Market/DAL_Bars.mqh>
#include <StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <M0001/DAL_M0001Engine.mqh>
#include <Execution/E0009/DAL_E0009Modules.mqh>
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

input group "00. SYMBOL / EXECUTION"
input string InpSection00 = "===== 00 | SYMBOL / EXECUTION =====";
input string InpSymbol = "";                         // Empty = current chart symbol
input bool InpTradingEnabled = true;                 // true = send real tester/live orders; false = plan/log only
input long InpMagicNumber = 9009009;
input string InpOrderCommentPrefix = "DALE9";
input bool InpRunOnInit = true;
input bool InpPrintLogs = true;
input bool InpPrintRejectLogs = true;

input group "01. MACRO MODE LEVEL"
input string InpSection01 = "===== 01 | MACRO MODE: H4 DEFAULT =====";
input bool InpUseMacroModeFilter = true;             // true = macro controls allowed direction
input ENUM_TIMEFRAMES InpMacroModeTF = PERIOD_H4;
input int InpMacroModeNodeCount = 4;                 // nearest valid chain: H1>H2>H3>H4 => SELL, L1<L2<L3<L4 => BUY
input int InpMacroModeL = 2;
input int InpMacroModeBars = 1000;
input int InpMacroModeMaxAgeBars = 0;                // 0 = no age limit

input group "02. MIDDLE SETUP LEVEL"
input string InpSection02 = "===== 02 | SETUP: M15 DEFAULT =====";
input ENUM_TIMEFRAMES InpSetupTF = PERIOD_M15;
input int InpSetupNodeCount = 4;                     // latest N only: H1>...=>SELL, L1<...=>BUY
input int InpSetupL = 2;
input int InpSetupBars = 1200;
input int InpSetupMaxAgeBars = 0;                    // 0 = no age limit
input bool InpRequireSetupAgreesWithMacro = true;    // true = macro direction and setup direction must match

input group "03. ENTRY HOOK LEVEL"
input string InpSection03 = "===== 03 | ENTRY: M1 HOOKS =====";
input ENUM_TIMEFRAMES InpExecutionTF = PERIOD_M1;
input int InpExecutionBars = 500;
input int InpExecutionL = 2;
input double InpZoneRatio = 0.90;                    // M1 hook zone ratio; compile fix: used by E0009_Config
input int InpM1HookMaxAgeBars = 40;                  // 0 = no hook age limit
input bool InpRequireFreshM1HookAfterSetupClose = true;
input bool InpRejectHuntedM1Hook = true;
input int InpMaxHookCandidatesPerBar = 0;              // 0 = scan all eligible hooks
input bool InpOneTradePerHookForever = true;         // one tester/session trade per exact hook key
input ENUM_DAL_E0009_ORDER_MODE InpOrderMode = DAL_E0009_ORDER_LIMIT_REVISIT; // limit touch on hook extreme

input group "04. MICRO-ONLY ENTRY FILTER"
input string InpSection04 = "===== 04 | MICRO-ONLY FILTER =====";
input bool InpUseMicroOnlyFilter = false;
input double InpMaxHookRiskToSetupAmplitude = 0.08;  // hook risk <= this ratio of setup amplitude
input int InpMicroAvgRangeBars = 80;
input double InpMaxHookRiskToM1AvgRange = 3.0;       // hook risk <= N x recent M1 average range
input int InpMaxHookRiskPoints = 0;                  // 0 = disabled

input group "05. EXIT LEVEL"
input string InpSection05 = "===== 05 | EXIT: INDEPENDENT TF PATTERN =====";
input ENUM_DAL_E0009_EXIT_MODE InpExitMode = DAL_E0009_EXIT_TF_MONOTONIC_PATTERN;
input ENUM_TIMEFRAMES InpExitTF = PERIOD_H4;
input int InpExitNodeCount = 3;                      // BUY exits on rising highs; SELL exits on falling lows
input int InpExitL = 2;
input int InpExitBars = 1000;
input int InpExitMaxAgeBars = 0;                     // 0 = no age limit
input bool InpUseCurrentExitPatternAsInitialTP = false;
input double InpFixedR = 50.0;                       // used only if InpExitMode = FIXED_R

input group "06. SPREAD / RISK / EXPOSURE"
input string InpSection06 = "===== 06 | SPREAD / RISK / EXPOSURE =====";
input double InpStopBehindNodeSpreadMultiplier = 1.0; // SL buffer behind M1 hook node
input double InpRiskCash = 100.0;
input bool InpAllowMinLotIfRiskTooSmall = false;
input double InpCommissionPerLotRoundTurn = 0.0;
input int InpMaxPendingPerSide = 0;                  // 0 = no cap
input int InpMaxPositionsPerSide = 0;                // 0 = no cap
input int InpUpdateEveryNExecutionBars = 1;

#define DAL_E0009_BUILD "1.12"

CTrade g_trade;
datetime g_last_execution_open_time = 0;
int g_execution_bar_counter = 0;

DALE0009PatternState g_macro_state;
DALE0009PatternState g_setup_state;
DALE0009PatternState g_exit_buy_state;
DALE0009PatternState g_exit_sell_state;

DALLRuleNode g_exit_nodes_cache[];
int g_exit_nodes_count_cache = 0;

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
   c.setup_L = MathMax(1, InpSetupL);
   c.zone_ratio = MathMax(0.0, MathMin(0.9999, InpZoneRatio));

   c.m1_max_hook_age_bars = MathMax(0, InpM1HookMaxAgeBars);
   c.require_fresh_m1_hook_after_setup_close = InpRequireFreshM1HookAfterSetupClose;
   c.reject_hunted_m1_hook = InpRejectHuntedM1Hook;
   c.max_hook_candidates_per_bar = MathMax(0, InpMaxHookCandidatesPerBar); // 0 = all hooks

   c.use_micro_only_filter = InpUseMicroOnlyFilter;
   c.max_hook_risk_to_setup_amplitude = MathMax(0.0, InpMaxHookRiskToSetupAmplitude);
   c.micro_avg_range_bars = MathMax(0, InpMicroAvgRangeBars);
   c.max_hook_risk_to_m1_avg_range = MathMax(0.0, InpMaxHookRiskToM1AvgRange);
   c.max_hook_risk_points = MathMax(0, InpMaxHookRiskPoints);

   c.fixed_r = MathMax(0.0, InpFixedR);
   c.exit_node_count = MathMax(1, InpExitNodeCount);

   c.stop_behind_node_spread_mult = MathMax(0.0, InpStopBehindNodeSpreadMultiplier);

   c.counter_mode = DAL_E0009_COUNTER_OPPOSITE_123;
   c.exit_mode = InpExitMode;
   c.order_mode = InpOrderMode;
   return c;
}

bool E0009_LoadPattern(
   const string symbol,
   const ENUM_TIMEFRAMES tf,
   const int bars_requested,
   const int L,
   const int required_count,
   const int max_age_bars,
   const ENUM_DAL_E0009_HTF_123_DIRECTION required_direction,
   const bool nearest_live_scan,
   DALE0009PatternState &state
)
{
   DALBar bars[];
   DALLRuleNode nodes[];
   int bars_count = 0;
   int nodes_count = 0;
   string reason = "";

   if(!DAL_E0009LoadNodes(symbol, tf, MathMax(200, bars_requested), MathMax(1, L), bars, bars_count, nodes, nodes_count, reason))
   {
      DAL_E0009_ResetPattern(state);
      state.tf = tf;
      state.required_count = required_count;
      state.reason = reason;
      return false;
   }

   if(required_direction == DAL_E0009_123_NONE)
   {
      if(nearest_live_scan)
         return DAL_E0009FindLatestMonotonicPatternAny(nodes, nodes_count, bars_count, tf, MathMax(1, required_count), MathMax(0, max_age_bars), state);

      return DAL_E0009FindLatestOnlyMonotonicPatternAny(nodes, nodes_count, bars_count, tf, MathMax(1, required_count), MathMax(0, max_age_bars), state);
   }

   if(nearest_live_scan)
      return DAL_E0009FindLatestMonotonicPatternOfType(nodes, nodes_count, bars_count, tf, MathMax(1, required_count), MathMax(0, max_age_bars), required_direction, state);

   return DAL_E0009FindLatestOnlyMonotonicPatternOfType(nodes, nodes_count, bars_count, tf, MathMax(1, required_count), MathMax(0, max_age_bars), required_direction, state);
}

bool E0009_LoadExitPatterns(const string symbol)
{
   DALBar bars[];
   DALLRuleNode nodes[];
   int bars_count = 0;
   int nodes_count = 0;
   string reason = "";

   if(!DAL_E0009LoadNodes(symbol, InpExitTF, MathMax(200, InpExitBars), MathMax(1, InpExitL), bars, bars_count, nodes, nodes_count, reason))
   {
      ArrayResize(g_exit_nodes_cache, 0);
      g_exit_nodes_count_cache = 0;
      DAL_E0009_ResetPattern(g_exit_buy_state);
      DAL_E0009_ResetPattern(g_exit_sell_state);
      g_exit_buy_state.tf = InpExitTF;
      g_exit_sell_state.tf = InpExitTF;
      g_exit_buy_state.reason = reason;
      g_exit_sell_state.reason = reason;
      return false;
   }

   ArrayResize(g_exit_nodes_cache, nodes_count);
   for(int k = 0; k < nodes_count; k++)
      g_exit_nodes_cache[k] = nodes[k];
   g_exit_nodes_count_cache = nodes_count;

   bool buy_exit = DAL_E0009FindLatestMonotonicPatternOfType(nodes, nodes_count, bars_count, InpExitTF, MathMax(1, InpExitNodeCount), MathMax(0, InpExitMaxAgeBars),
                                                             DAL_E0009_123_HIGHER_HIGHS, g_exit_buy_state);
   bool sell_exit = DAL_E0009FindLatestMonotonicPatternOfType(nodes, nodes_count, bars_count, InpExitTF, MathMax(1, InpExitNodeCount), MathMax(0, InpExitMaxAgeBars),
                                                              DAL_E0009_123_LOWER_LOWS, g_exit_sell_state);

   return (buy_exit || sell_exit);
}

bool E0009_GetCurrentExitTP(const int direction, const double entry, double &tp)
{
   tp = 0.0;

   if(InpExitMode != DAL_E0009_EXIT_TF_MONOTONIC_PATTERN)
      return false;

   if(direction > 0)
   {
      if(!g_exit_buy_state.valid)
         return false;
      tp = g_exit_buy_state.p3.price;
      return (tp > entry);
   }
   else if(direction < 0)
   {
      if(!g_exit_sell_state.valid)
         return false;
      tp = g_exit_sell_state.p3.price;
      return (tp < entry);
   }

   return false;
}

bool E0009_CheckPositionTPGeometry(const string symbol, const int direction, const double tp)
{
   if(tp <= 0.0)
      return false;

   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   int stops_level = (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL);
   double min_dist = MathMax(0.0, stops_level * point);

   if(direction > 0)
      return (tp > bid + min_dist);
   if(direction < 0)
      return (tp < ask - min_dist);

   return false;
}

bool E0009_PricesCloseEnough(const string symbol, const double a, const double b)
{
   return AL_UC04PricesCloseEnough(symbol, a, b);
}

void E0009_SyncGlobalExitTP(
   const string symbol,
   int &checked,
   int &modified,
   int &waiting,
   int &rejected
)
{
   checked = 0;
   modified = 0;
   waiting = 0;
   rejected = 0;

   if(InpExitMode != DAL_E0009_EXIT_TF_MONOTONIC_PATTERN)
      return;

   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != InpMagicNumber)
         continue;

      string comment = PositionGetString(POSITION_COMMENT);
      if(InpOrderCommentPrefix != "" && StringFind(comment, InpOrderCommentPrefix, 0) != 0)
         continue;

      ENUM_POSITION_TYPE pos_type = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
      int direction = (pos_type == POSITION_TYPE_BUY ? +1 : (pos_type == POSITION_TYPE_SELL ? -1 : 0));
      if(direction == 0)
         continue;

      checked++;

      double entry = PositionGetDouble(POSITION_PRICE_OPEN);
      double sl = PositionGetDouble(POSITION_SL);
      double old_tp = PositionGetDouble(POSITION_TP);

      double new_tp = 0.0;
      if(!E0009_GetCurrentExitTP(direction, entry, new_tp))
      {
         waiting++;
         continue;
      }

      int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
      new_tp = NormalizeDouble(new_tp, digits);

      if(E0009_PricesCloseEnough(symbol, old_tp, new_tp))
         continue;

      if(!E0009_CheckPositionTPGeometry(symbol, direction, new_tp))
      {
         rejected++;
         continue;
      }

      g_trade.SetExpertMagicNumber(InpMagicNumber);
      if(g_trade.PositionModify(ticket, sl, new_tp))
         modified++;
      else
         rejected++;
   }
}

void E0009_Process(const string run_mode)
{
   string symbol = E0009_Symbol();
   DALE0009Config cfg = E0009_Config();
   DALE0009Diagnostics diag;
   DAL_E0009_ResetDiagnostics(diag);

   bool macro_ok = true;
   if(InpUseMacroModeFilter)
   {
      macro_ok = E0009_LoadPattern(symbol, InpMacroModeTF, InpMacroModeBars, InpMacroModeL, InpMacroModeNodeCount, InpMacroModeMaxAgeBars,
                                   DAL_E0009_123_NONE, true, g_macro_state); // macro scans nearest valid chain from live edge
      if(macro_ok && g_macro_state.valid)
         diag.macro_ok++;
      else
         diag.macro_missing++;
   }
   else
   {
      DAL_E0009_ResetPattern(g_macro_state);
      macro_ok = true;
   }

   bool setup_ok = E0009_LoadPattern(symbol, InpSetupTF, InpSetupBars, InpSetupL, InpSetupNodeCount, InpSetupMaxAgeBars,
                                     DAL_E0009_123_NONE, false, g_setup_state); // setup checks only latest N highs/lows
   if(setup_ok && g_setup_state.valid)
      diag.setup_ok++;
   else
      diag.setup_missing++;

   if(!macro_ok || !setup_ok || !g_setup_state.valid)
   {
      if(InpPrintLogs && InpPrintRejectLogs)
         Print("DAL_E0009_SKIP *** build=", DAL_E0009_BUILD,
            "*runMode=", run_mode,
            "*reason=macro_or_setup_missing",
            "*macroOk=", DAL_BoolToString(macro_ok),
            "*setupOk=", DAL_BoolToString(setup_ok),
            "*macroReason=", g_macro_state.reason,
            "*setupReason=", g_setup_state.reason);
      return;
   }

   int macro_dir = (InpUseMacroModeFilter ? DAL_E0009TradeDirectionFromPattern(g_macro_state) : 0);
   int setup_dir = DAL_E0009TradeDirectionFromPattern(g_setup_state);
   int trade_direction = setup_dir;

   if(InpUseMacroModeFilter && macro_dir != 0)
   {
      if(InpRequireSetupAgreesWithMacro && setup_dir != macro_dir)
      {
         diag.macro_conflict++;
         diag.setup_conflict++;
         if(InpPrintLogs && InpPrintRejectLogs)
            Print("DAL_E0009_SKIP *** build=", DAL_E0009_BUILD,
               "*runMode=", run_mode,
               "*reason=macro_setup_direction_conflict",
               "*macroDir=", macro_dir,
               "*setupDir=", setup_dir,
               "*macroMode=", DAL_E0009DirectionName(g_macro_state.direction),
               "*setupMode=", DAL_E0009DirectionName(g_setup_state.direction));
         return;
      }

      trade_direction = macro_dir;
   }

   E0009_LoadExitPatterns(symbol);

   int tp_checked = 0, tp_modified = 0, tp_waiting = 0, tp_rejected = 0;
   E0009_SyncGlobalExitTP(symbol, tp_checked, tp_modified, tp_waiting, tp_rejected);

   DALBar m1_bars[];
   DALLRuleNode m1_nodes[];
   int m1_bars_count = 0;
   int m1_nodes_count = 0;
   string reason = "";

   if(!DAL_E0009LoadNodes(symbol, InpExecutionTF, MathMax(200, InpExecutionBars), MathMax(1, InpExecutionL), m1_bars, m1_bars_count, m1_nodes, m1_nodes_count, reason))
   {
      diag.m1_map_failed++;
      if(InpPrintLogs && InpPrintRejectLogs)
         Print("DAL_E0009_SKIP *** build=", DAL_E0009_BUILD,
            "*runMode=", run_mode,
            "*reason=m1_map_failed",
            "*detail=", reason);
      return;
   }

   diag.m1_map_ok++;

   DALE0009HookSignal signals[];
   int signals_count = DAL_E0009CollectHookSignals(symbol, m1_bars, m1_bars_count, m1_nodes, m1_nodes_count,
                                                   g_setup_state, trade_direction, cfg, signals, diag);

   int planned = 0;
   int sent = 0;
   int rejected = 0;

   if(signals_count <= 0)
   {
      rejected++;
      if(InpPrintLogs && InpPrintRejectLogs)
         Print("DAL_E0009_HOOK_REJECT *** build=", DAL_E0009_BUILD,
            "*dir=", trade_direction,
            "*reason=no_valid_hook_signal",
            "*setup=", DAL_E0009DirectionName(g_setup_state.direction),
            "*seen=", diag.hook_seen,
            "*afterTimeReject=", diag.hook_after_time_reject,
            "*ageReject=", diag.hook_age_reject,
            "*zoneFail=", diag.hook_zone_failed,
            "*huntedReject=", diag.hook_hunted_reject,
            "*microReject=", diag.hook_micro_reject);
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

      if(InpUseCurrentExitPatternAsInitialTP && InpExitMode == DAL_E0009_EXIT_TF_MONOTONIC_PATTERN)
      {
         double init_tp = 0.0;
         if(E0009_GetCurrentExitTP(sig.direction, sig.entry, init_tp))
         {
            int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
            sig.tp = NormalizeDouble(init_tp, digits);
            sig.potential_r = MathAbs(sig.tp - sig.entry) / MathMax(sig.risk_distance, SymbolInfoDouble(symbol, SYMBOL_POINT));
         }
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
               "*macroDir=", macro_dir,
               "*setupDir=", setup_dir,
               "*tradeDir=", sig.direction,
               "*hookNode=", sig.hook_node.id,
               "*hookType=", (sig.hook_node.type == DAL_NODE_LOW ? "LOW" : "HIGH"),
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

   if(InpPrintLogs)
   {
      Print("DAL_E0009_AUDIT_A *** build=", DAL_E0009_BUILD,
         "*runMode=", run_mode,
         "*symbol=", symbol,
         "*macroTF=", EnumToString(InpMacroModeTF),
         "*setupTF=", EnumToString(InpSetupTF),
         "*entryTF=", EnumToString(InpExecutionTF),
         "*exitTF=", EnumToString(InpExitTF),
         "*macroMode=", DAL_E0009DirectionName(g_macro_state.direction),
         "*setupMode=", DAL_E0009DirectionName(g_setup_state.direction),
         "*macroDir=", macro_dir,
         "*setupDir=", setup_dir,
         "*tradeDir=", trade_direction);

      Print("DAL_E0009_AUDIT_B *** build=", DAL_E0009_BUILD,
         "*macroN=", InpMacroModeNodeCount,
         "*setupN=", InpSetupNodeCount,
         "*exitN=", InpExitNodeCount,
         "*hookSeen=", diag.hook_seen,
         "*hookAfterTimeReject=", diag.hook_after_time_reject,
         "*hookAgeReject=", diag.hook_age_reject,
         "*hookZoneFail=", diag.hook_zone_failed,
         "*hookHuntedReject=", diag.hook_hunted_reject,
         "*hookMicroReject=", diag.hook_micro_reject,
         "*hookBuilt=", diag.hook_built);

      Print("DAL_E0009_AUDIT_C *** build=", DAL_E0009_BUILD,
         "*microFilter=", DAL_BoolToString(cfg.use_micro_only_filter),
         "*maxRiskToSetup=", DoubleToString(cfg.max_hook_risk_to_setup_amplitude, 4),
         "*maxRiskToM1Avg=", DoubleToString(cfg.max_hook_risk_to_m1_avg_range, 2),
         "*geometryReject=", diag.geometry_reject,
         "*riskReject=", diag.risk_reject,
         "*capReject=", diag.cap_reject,
         "*duplicateSkip=", diag.duplicate_skip,
         "*usedHookKeys=", g_used_hook_keys_count,
         "*planned=", planned,
         "*sentOrPlan=", sent,
         "*rejected=", rejected);

      Print("DAL_E0009_AUDIT_D *** build=", DAL_E0009_BUILD,
         "*buyExitValid=", DAL_BoolToString(g_exit_buy_state.valid),
         "*buyExitPrice=", DoubleToString(g_exit_buy_state.p3.price, _Digits),
         "*sellExitValid=", DAL_BoolToString(g_exit_sell_state.valid),
         "*sellExitPrice=", DoubleToString(g_exit_sell_state.p3.price, _Digits),
         "*tpChecked=", tp_checked,
         "*tpModified=", tp_modified,
         "*tpWaiting=", tp_waiting,
         "*tpRejected=", tp_rejected);
   }
}

int OnInit()
{
   g_trade.SetExpertMagicNumber(InpMagicNumber);

   DAL_E0009_ResetPattern(g_macro_state);
   DAL_E0009_ResetPattern(g_setup_state);
   DAL_E0009_ResetPattern(g_exit_buy_state);
   DAL_E0009_ResetPattern(g_exit_sell_state);
   ArrayResize(g_exit_nodes_cache, 0);
   g_exit_nodes_count_cache = 0;

   ArrayResize(g_used_hook_keys, 0);
   g_used_hook_keys_count = 0;

   Print("DAL_E0009_BUILD_SANITY *** build=", DAL_E0009_BUILD,
      "*module=MULTI_LEVEL_MONOTONIC_SWING_HOOK",
      "*macroTF=", EnumToString(InpMacroModeTF),
      "*macroN=", InpMacroModeNodeCount,
      "*setupTF=", EnumToString(InpSetupTF),
      "*setupN=", InpSetupNodeCount,
      "*entryTF=", EnumToString(InpExecutionTF),
      "*exitTF=", EnumToString(InpExitTF),
      "*exitN=", InpExitNodeCount,
      "*orderMode=", DAL_E0009OrderModeName(InpOrderMode),
      "*exitMode=", DAL_E0009ExitModeName(InpExitMode),
      "*microFilter=", DAL_BoolToString(InpUseMicroOnlyFilter),
      "*oneTradePerHook=", DAL_BoolToString(InpOneTradePerHookForever),
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
   g_execution_bar_counter++;

   int every = MathMax(1, InpUpdateEveryNExecutionBars);
   if((g_execution_bar_counter % every) != 0)
      return;

   E0009_Process("NEW_EXECUTION_BAR");
}
