//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0008 MTF Purple Extreme Executor            |
//| Multi-timeframe source-context + micro extreme trigger template.  |
//+------------------------------------------------------------------+
#property strict
#property version   "1.01"
#property description "E0008: MTF purple/source context executor for tiny-stop high-R entries."

#include <Trade/Trade.mqh>
#include <Market/DAL_Bars.mqh>
#include <StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <M0001/DAL_M0001Config.mqh>
#include <M0001/DAL_M0001Engine.mqh>
#include <Execution/E0008/DAL_E0008Modules.mqh>

input string InpSymbol = "";

// Timeframe stack.
input ENUM_TIMEFRAMES InpExecutionTF = PERIOD_M1;
input ENUM_TIMEFRAMES InpLocalContextTF = PERIOD_M15;
input bool InpUseContextTF1 = true;
input ENUM_TIMEFRAMES InpContextTF1 = PERIOD_H1;
input bool InpUseContextTF2 = true;
input ENUM_TIMEFRAMES InpContextTF2 = PERIOD_M15;
input bool InpUseContextTF3 = false;
input ENUM_TIMEFRAMES InpContextTF3 = PERIOD_H4;

// L=2 because the purple examples were generated with L=2.
input int InpContextL = 2;
input int InpExecutionL = 2;
input double InpZoneRatio = 0.90;
input int InpBarsPerTF = 3500;          // legacy fallback only
input int InpContextBarsPerTF = 1800;    // HTF context bars; cached by TF bar
input int InpLocalBars = 1200;           // local context bars; cached by local TF bar
input int InpExecutionBars = 700;        // execution TF bars; rebuilt once per execution candle
input int InpExitGap = 6;
input int InpMaxEvents = 2500;
input bool InpCacheContextMaps = true;
input bool InpUpdateContextOnlyOnItsOwnNewBar = true;
input int InpForceContextRefreshEveryExecBars = 0; // 0 = off
input int InpSyncTPEveryNBars = 1;

// Source / purple proxy.
// 0 = live/no-future source mode.
// 500 = oracle purple-class research mode.
input int InpMinSourceSurvivalBars = 0;
input double InpMinFirstReactionR = 2.0;
input bool InpRequireFirstTouchNotHunted = true;
input bool InpAllowAlreadySecondRevisitForResearch = false;
input int InpMaxSourceAgeBars = 2500;

// MTF alignment.
input int InpMinAlignedContexts = 2;
input bool InpRejectIfAnyContextConflicts = true;
input bool InpRequireLocalContext = true;

// Entry/stop/target modes.
input ENUM_DAL_E0008_ENTRY_MODE InpEntryMode = DAL_E0008_ENTRY_MICRO_NODE_REVISIT;
input ENUM_DAL_E0008_STOP_MODE InpStopMode = DAL_E0008_STOP_MICRO_NODE;
input ENUM_DAL_E0008_TARGET_MODE InpTargetMode = DAL_E0008_TARGET_CONTEXT_DESTINATION;

// Asymmetry: this is the real gate for the 50R/100R style.
input double InpMinPotentialR = 50.0;
input double InpFixedRewardR = 100.0;
input int InpOppositeNodeTPCount = 3;

input int InpMaxMicroNodeAgeBars = 250;
input int InpDestinationLookbackBars = 1800;

// Spread handling.
input double InpBuyEntrySpreadMultiplier = 1.0;
input double InpSellStopSpreadMultiplier = 1.0;

// Risk / exposure.
input long InpMagicNumber = 8008008;
input string InpOrderCommentPrefix = "DALE8";
input double InpRiskCash = 100.0;
input bool InpAllowMinLotIfRiskTooSmall = false;
input double InpCommissionPerLotRoundTurn = 0.0;
input int InpMaxBuyPending = 1;
input int InpMaxSellPending = 1;
input int InpMaxBuyPositions = 1;
input int InpMaxSellPositions = 1;

input bool InpTradingEnabled = false; // default plan-only until reports look right
input bool InpRunOnInit = true;
input int InpUpdateEveryNBars = 1;
input bool InpPrintLogs = true;
input bool InpPrintSkipLogs = false;
input bool InpPrintPlanLogs = true;

#define DAL_E0008_BUILD "1.01"

CTrade g_trade;
datetime g_last_bar_time = 0;
int g_new_bar_counter = 0;

DALE0008ContextState g_ctx1_cache;
DALE0008ContextState g_ctx2_cache;
DALE0008ContextState g_ctx3_cache;
DALE0008ContextState g_local_cache;

datetime g_ctx1_open_time = 0;
datetime g_ctx2_open_time = 0;
datetime g_ctx3_open_time = 0;
datetime g_local_open_time = 0;

bool g_ctx1_evaluated = false;
bool g_ctx2_evaluated = false;
bool g_ctx3_evaluated = false;
bool g_local_evaluated = false;

string E0008_Symbol()
{
   return (InpSymbol == "" ? _Symbol : InpSymbol);
}

ENUM_TIMEFRAMES E0008_ExecutionTF()
{
   return (InpExecutionTF == PERIOD_CURRENT ? (ENUM_TIMEFRAMES)_Period : InpExecutionTF);
}

int E0008_ContextBarsRequest()
{
   int v = (InpContextBarsPerTF > 0 ? InpContextBarsPerTF : InpBarsPerTF);
   return MathMax(300, v);
}

int E0008_LocalBarsRequest()
{
   int v = (InpLocalBars > 0 ? InpLocalBars : InpBarsPerTF);
   return MathMax(300, v);
}

int E0008_ExecutionBarsRequest()
{
   int v = (InpExecutionBars > 0 ? InpExecutionBars : InpBarsPerTF);
   return MathMax(200, v);
}

void E0008_FillPolicies(
   DALE0008SourcePolicy &source,
   DALE0008MTFPolicy &mtf,
   DALE0008ExecutionPolicy &exec,
   DALE0008ExposurePolicy &exposure
)
{
   DAL_E0008_DefaultSourcePolicy(source);
   source.L = MathMax(1, InpContextL);
   source.zone_ratio = MathMax(0.0, MathMin(0.9999, InpZoneRatio));
   source.exit_gap = MathMax(1, InpExitGap);
   source.max_events = MathMax(1, InpMaxEvents);
   source.min_source_survival_bars = MathMax(0, InpMinSourceSurvivalBars);
   source.min_first_reaction_r = MathMax(0.0, InpMinFirstReactionR);
   source.require_first_touch_not_hunted = InpRequireFirstTouchNotHunted;
   source.allow_already_second_revisit_for_research = InpAllowAlreadySecondRevisitForResearch;
   source.max_source_age_bars = MathMax(0, InpMaxSourceAgeBars);

   DAL_E0008_DefaultMTFPolicy(mtf);
   mtf.min_aligned_contexts = MathMax(1, InpMinAlignedContexts);
   mtf.reject_if_any_context_conflicts = InpRejectIfAnyContextConflicts;
   mtf.require_local_context = InpRequireLocalContext;

   DAL_E0008_DefaultExecutionPolicy(exec);
   exec.entry_mode = InpEntryMode;
   exec.stop_mode = InpStopMode;
   exec.target_mode = InpTargetMode;
   exec.min_potential_r = MathMax(0.0, InpMinPotentialR);
   exec.fixed_reward_r = MathMax(0.0, InpFixedRewardR);
   exec.opposite_node_tp_count = MathMax(1, InpOppositeNodeTPCount);
   exec.buy_entry_spread_mult = MathMax(0.0, InpBuyEntrySpreadMultiplier);
   exec.sell_stop_spread_mult = MathMax(0.0, InpSellStopSpreadMultiplier);
   exec.micro_L = MathMax(1, InpExecutionL);
   exec.max_micro_node_age_bars = MathMax(1, InpMaxMicroNodeAgeBars);

   DAL_E0008_DefaultExposurePolicy(exposure);
   exposure.max_buy_pending = MathMax(0, InpMaxBuyPending);
   exposure.max_sell_pending = MathMax(0, InpMaxSellPending);
   exposure.max_buy_positions = MathMax(0, InpMaxBuyPositions);
   exposure.max_sell_positions = MathMax(0, InpMaxSellPositions);
}

bool E0008_BuildContextForTF(
   const string symbol,
   const ENUM_TIMEFRAMES tf,
   const int bars_requested,
   const DALE0008SourcePolicy &source,
   DALE0008ContextState &ctx
)
{
   DALBar bars[];
   DALLRuleNode nodes[];
   DALM0001Event events[];
   int bars_count = 0, nodes_count = 0, events_count = 0;
   string reason = "";

   if(!DAL_E0008_LoadM0001Map(symbol, tf, bars_requested, source.L, source.zone_ratio, source.exit_gap, source.max_events,
                              bars, bars_count, nodes, nodes_count, events, events_count, reason))
   {
      DAL_E0008_ResetContext(ctx);
      ctx.tf = tf;
      ctx.reason = reason;
      return false;
   }

   if(!DAL_E0008_BuildBestContextFromMap(tf, bars, bars_count, events, events_count, source, InpDestinationLookbackBars, ctx))
      return false;

   return true;
}

bool E0008_UpdateContextCacheForTF(
   const string symbol,
   const ENUM_TIMEFRAMES tf,
   const bool use_tf,
   const int bars_requested,
   const DALE0008SourcePolicy &source,
   const bool force_refresh,
   DALE0008ContextState &cache,
   datetime &cache_open_time,
   bool &cache_evaluated
)
{
   if(!use_tf)
   {
      DAL_E0008_ResetContext(cache);
      cache.tf = tf;
      cache.reason = "disabled";
      cache_evaluated = false;
      cache_open_time = 0;
      return false;
   }

   datetime open_time = iTime(symbol, tf, 0);
   if(open_time <= 0)
   {
      DAL_E0008_ResetContext(cache);
      cache.tf = tf;
      cache.reason = "tf_open_time_unavailable";
      cache_evaluated = true;
      cache_open_time = 0;
      return false;
   }

   bool must_refresh = force_refresh
      || !InpCacheContextMaps
      || !cache_evaluated
      || !InpUpdateContextOnlyOnItsOwnNewBar
      || cache_open_time != open_time;

   if(must_refresh)
   {
      E0008_BuildContextForTF(symbol, tf, bars_requested, source, cache);
      cache.tf = tf;
      cache_open_time = open_time;
      cache_evaluated = true;
   }

   return cache.valid;
}

bool E0008_BuildLocalContextAndExecutionMap(
   const string symbol,
   const DALE0008SourcePolicy &source,
   DALE0008ContextState &local,
   DALBar &exec_bars[],
   int &exec_bars_count,
   DALLRuleNode &exec_nodes[],
   int &exec_nodes_count,
   DALM0001Event &exec_events[],
   int &exec_events_count,
   string &reason
)
{
   // Local context map.
   DALBar local_bars[];
   DALLRuleNode local_nodes[];
   DALM0001Event local_events[];
   int local_bars_count = 0, local_nodes_count = 0, local_events_count = 0;

   if(!DAL_E0008_LoadM0001Map(symbol, InpLocalContextTF, E0008_LocalBarsRequest(), source.L, source.zone_ratio, source.exit_gap, source.max_events,
                              local_bars, local_bars_count, local_nodes, local_nodes_count, local_events, local_events_count, reason))
   {
      DAL_E0008_ResetContext(local);
      local.tf = InpLocalContextTF;
      local.reason = reason;
      return false;
   }

   if(!DAL_E0008_BuildBestContextFromMap(InpLocalContextTF, local_bars, local_bars_count, local_events, local_events_count, source, InpDestinationLookbackBars, local))
   {
      reason = local.reason;
      return false;
   }

   // Execution map.
   ENUM_TIMEFRAMES exec_tf = E0008_ExecutionTF();
   if(!DAL_E0008_LoadM0001Map(symbol, exec_tf, E0008_ExecutionBarsRequest(), MathMax(1, InpExecutionL), source.zone_ratio, source.exit_gap, source.max_events,
                              exec_bars, exec_bars_count, exec_nodes, exec_nodes_count, exec_events, exec_events_count, reason))
      return false;

   return true;
}

void E0008_Process(const string run_mode)
{
   string symbol = E0008_Symbol();

   DALE0008SourcePolicy source;
   DALE0008MTFPolicy mtf;
   DALE0008ExecutionPolicy exec;
   DALE0008ExposurePolicy exposure;
   E0008_FillPolicies(source, mtf, exec, exposure);

   DALE0008ContextState c1, c2, c3, primary, local;
   bool force_context_refresh = (run_mode == "INIT")
      || (InpForceContextRefreshEveryExecBars > 0 && (g_new_bar_counter % InpForceContextRefreshEveryExecBars) == 0);

   E0008_UpdateContextCacheForTF(symbol, InpContextTF1, InpUseContextTF1, E0008_ContextBarsRequest(), source, force_context_refresh,
                                 g_ctx1_cache, g_ctx1_open_time, g_ctx1_evaluated);
   E0008_UpdateContextCacheForTF(symbol, InpContextTF2, InpUseContextTF2, E0008_ContextBarsRequest(), source, force_context_refresh,
                                 g_ctx2_cache, g_ctx2_open_time, g_ctx2_evaluated);
   E0008_UpdateContextCacheForTF(symbol, InpContextTF3, InpUseContextTF3, E0008_ContextBarsRequest(), source, force_context_refresh,
                                 g_ctx3_cache, g_ctx3_open_time, g_ctx3_evaluated);

   c1 = g_ctx1_cache;
   c2 = g_ctx2_cache;
   c3 = g_ctx3_cache;

   if(!DAL_E0008_SelectPrimaryContext(c1, InpUseContextTF1, c2, InpUseContextTF2, c3, InpUseContextTF3, primary))
   {
      if(InpPrintLogs && InpPrintSkipLogs)
         Print("DAL_E0008_SKIP *** build=", DAL_E0008_BUILD, "*runMode=", run_mode, "*reason=no_primary_context",
            "*c1=", c1.reason, "*c2=", c2.reason, "*c3=", c3.reason);
      return;
   }

   bool has_conflict = false;
   int aligned = DAL_E0008_CountAlignedContexts(c1, InpUseContextTF1, c2, InpUseContextTF2, c3, InpUseContextTF3,
                                                primary.direction, mtf.reject_if_any_context_conflicts, has_conflict);

   if(aligned < mtf.min_aligned_contexts)
   {
      if(InpPrintLogs && InpPrintSkipLogs)
         Print("DAL_E0008_SKIP *** build=", DAL_E0008_BUILD, "*runMode=", run_mode,
            "*reason=mtf_alignment_failed",
            "*primaryDir=", primary.direction,
            "*aligned=", aligned,
            "*required=", mtf.min_aligned_contexts,
            "*conflict=", DAL_BoolToString(has_conflict));
      return;
   }

   string load_reason = "";

   bool local_ok = E0008_UpdateContextCacheForTF(symbol, InpLocalContextTF, true, E0008_LocalBarsRequest(), source, force_context_refresh,
                                                g_local_cache, g_local_open_time, g_local_evaluated);
   local = g_local_cache;

   DALBar exec_bars[];
   DALLRuleNode exec_nodes[];
   DALM0001Event exec_events[];
   int exec_bars_count=0, exec_nodes_count=0, exec_events_count=0;

   ENUM_TIMEFRAMES exec_tf = E0008_ExecutionTF();
   bool exec_ok = DAL_E0008_LoadM0001Map(symbol, exec_tf, E0008_ExecutionBarsRequest(), MathMax(1, InpExecutionL),
                                         source.zone_ratio, source.exit_gap, source.max_events,
                                         exec_bars, exec_bars_count, exec_nodes, exec_nodes_count, exec_events, exec_events_count, load_reason);

   if(!local_ok || !exec_ok)
   {
      if(mtf.require_local_context || !exec_ok)
      {
         if(InpPrintLogs && InpPrintSkipLogs)
            Print("DAL_E0008_SKIP *** build=", DAL_E0008_BUILD, "*runMode=", run_mode,
               "*reason=local_or_exec_map_failed",
               "*localOk=", DAL_BoolToString(local_ok),
               "*execOk=", DAL_BoolToString(exec_ok),
               "*loadReason=", load_reason,
               "*localReason=", local.reason);
         return;
      }
      local = primary;
   }

   if(local.valid && local.direction != primary.direction)
   {
      if(InpPrintLogs && InpPrintSkipLogs)
         Print("DAL_E0008_SKIP *** build=", DAL_E0008_BUILD, "*runMode=", run_mode,
            "*reason=local_context_conflict",
            "*primaryDir=", primary.direction,
            "*localDir=", local.direction);
      return;
   }

   // Sync open-position TP only when target mode is opposite node.
   int tp_checked=0, tp_modified=0, tp_waiting=0, tp_rejected=0;
   bool should_sync_tp = (InpSyncTPEveryNBars <= 1) || ((g_new_bar_counter % MathMax(1, InpSyncTPEveryNBars)) == 0);
   if(exec.target_mode == DAL_E0008_TARGET_NTH_OPPOSITE_NODE && should_sync_tp)
      DAL_E0008SyncOppositeNodeTP(symbol, InpMagicNumber, InpOrderCommentPrefix, exec_nodes, exec_nodes_count,
                                  exec.opposite_node_tp_count, g_trade,
                                  tp_checked, tp_modified, tp_waiting, tp_rejected);

   ENUM_DAL_E0008_ENTRY_MODE modes[4];
   int modes_count = 1;
   modes[0] = exec.entry_mode;
   if(exec.entry_mode == DAL_E0008_ENTRY_ALL_MODES)
   {
      modes_count = 4;
      modes[0] = DAL_E0008_ENTRY_MICRO_NODE_REVISIT;
      modes[1] = DAL_E0008_ENTRY_LOCAL_SOURCE_REVISIT;
      modes[2] = DAL_E0008_ENTRY_LOCAL_SECONDARY_NODE;
      modes[3] = DAL_E0008_ENTRY_EARLY_LADDER_STEP;
   }

   int planned = 0, sent = 0, rejected = 0;

   for(int m = 0; m < modes_count; m++)
   {
      DALE0008MicroTrigger trigger;
      if(!DAL_E0008_BuildMicroTrigger(symbol, exec_bars, exec_bars_count, exec_nodes, exec_nodes_count, local, exec, source, modes[m], trigger))
      {
         rejected++;
         if(InpPrintLogs && InpPrintSkipLogs)
            Print("DAL_E0008_TRIGGER_REJECT *** build=", DAL_E0008_BUILD,
               "*mode=", DAL_E0008EntryModeName(modes[m]),
               "*reason=", trigger.reason);
         continue;
      }

      DALE0008TradePlan plan;
      if(!DAL_E0008_BuildTradePlan(symbol, primary, local, trigger, exec, plan))
      {
         rejected++;
         if(InpPrintLogs && InpPrintSkipLogs)
            Print("DAL_E0008_PLAN_REJECT *** build=", DAL_E0008_BUILD,
               "*mode=", DAL_E0008EntryModeName(modes[m]),
               "*reason=", plan.reason,
               "*triggerReason=", trigger.reason);
         continue;
      }

      planned++;

      string send_reason = "plan_only";
      bool ok = true;
      if(InpTradingEnabled)
         ok = DAL_E0008SendPlanLimit(symbol, InpMagicNumber, InpOrderCommentPrefix, InpRiskCash,
                                     InpCommissionPerLotRoundTurn, InpAllowMinLotIfRiskTooSmall,
                                     exposure, plan, g_trade, send_reason);

      if(ok)
      {
         sent++;
         if(InpPrintLogs && InpPrintPlanLogs)
            Print("DAL_E0008_PLAN *** build=", DAL_E0008_BUILD,
               "*runMode=", run_mode,
               "*mode=", DAL_E0008EntryModeName(plan.entry_mode),
               "*stopMode=", DAL_E0008StopModeName(plan.stop_mode),
               "*targetMode=", DAL_E0008TargetModeName(plan.target_mode),
               "*dir=", plan.direction,
               "*ctxTF=", EnumToString(plan.context_tf),
               "*localTF=", EnumToString(plan.local_tf),
               "*ctxNode=", plan.context_node_id,
               "*localNode=", plan.local_node_id,
               "*microNode=", plan.micro_node_id,
               "*entry=", DoubleToString(plan.entry, _Digits),
               "*sl=", DoubleToString(plan.sl, _Digits),
               "*tp=", DoubleToString(plan.tp, _Digits),
               "*risk=", DoubleToString(plan.risk_distance, _Digits),
               "*dest=", DoubleToString(plan.destination_price, _Digits),
               "*R=", DoubleToString(plan.potential_r, 2),
               "*comment=", plan.comment,
               "*send=", send_reason);
      }
      else
      {
         rejected++;
         if(InpPrintLogs && InpPrintSkipLogs)
            Print("DAL_E0008_SEND_REJECT *** build=", DAL_E0008_BUILD,
               "*mode=", DAL_E0008EntryModeName(plan.entry_mode),
               "*reason=", send_reason);
      }
   }

   if(InpPrintLogs)
   {
      Print("DAL_E0008_AUDIT *** build=", DAL_E0008_BUILD,
         "*runMode=", run_mode,
         "*symbol=", symbol,
         "*execTF=", EnumToString(E0008_ExecutionTF()),
         "*Lctx=", source.L,
         "*Lexe=", exec.micro_L,
         "*contextBars=", E0008_ContextBarsRequest(),
         "*localBars=", E0008_LocalBarsRequest(),
         "*executionBars=", E0008_ExecutionBarsRequest(),
         "*cache=", DAL_BoolToString(InpCacheContextMaps),
         "*primaryTF=", EnumToString(primary.tf),
         "*primaryDir=", primary.direction,
         "*primaryRole=", DAL_E0008RoleName(primary.role),
         "*primaryScore=", DoubleToString(primary.context_score, 2),
         "*aligned=", aligned,
         "*localTF=", EnumToString(local.tf),
         "*localRole=", DAL_E0008RoleName(local.role),
         "*entryMode=", DAL_E0008EntryModeName(exec.entry_mode),
         "*minR=", DoubleToString(exec.min_potential_r, 2),
         "*planned=", planned,
         "*sentOrPlan=", sent,
         "*rejected=", rejected,
         "*tpChecked=", tp_checked,
         "*tpModified=", tp_modified,
         "*tpWaiting=", tp_waiting,
         "*tpRejected=", tp_rejected);
   }
}

int OnInit()
{
   g_trade.SetExpertMagicNumber(InpMagicNumber);

   Print("DAL_E0008_BUILD_SANITY *** build=", DAL_E0008_BUILD,
      "*module=MTF_PURPLE_EXTREME_EXECUTOR",
      "*goal=tiny_stop_50R_100R_purple_source_hunt",
      "*defaultContextL=2",
      "*defaultExecutionL=2",
      "*entryMode=", DAL_E0008EntryModeName(InpEntryMode),
      "*targetMode=", DAL_E0008TargetModeName(InpTargetMode),
      "*tradingEnabled=", DAL_BoolToString(InpTradingEnabled));

   if(InpRunOnInit)
      E0008_Process("INIT");

   return INIT_SUCCEEDED;
}

void OnTick()
{
   string symbol = E0008_Symbol();
   ENUM_TIMEFRAMES tf = E0008_ExecutionTF();

   datetime open_time = iTime(symbol, tf, 0);
   if(open_time <= 0)
      return;
   if(open_time == g_last_bar_time)
      return;

   g_last_bar_time = open_time;
   g_new_bar_counter++;

   int every = MathMax(1, InpUpdateEveryNBars);
   if((g_new_bar_counter % every) != 0)
      return;

   E0008_Process("NEW_BAR");
}
