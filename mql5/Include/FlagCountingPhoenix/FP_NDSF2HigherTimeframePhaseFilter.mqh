#ifndef __FP_NDS_F2_HIGHER_TIMEFRAME_PHASE_FILTER_MQH__
#define __FP_NDS_F2_HIGHER_TIMEFRAME_PHASE_FILTER_MQH__
#property strict

#include "FP_Timebase.mqh"
#include "FP_NodeScaleList.mqh"
#include "FP_SequenceEngine.mqh"

#define FP_NDS_F2_HTF_PHASE_FILTER_VERSION "NDS-F2-HTF-F-PHASE-01"

enum FP_NDSF2HigherTimeframePhaseState
{
   FP_NDS_F2_HTF_PHASE_DISABLED = 0,
   FP_NDS_F2_HTF_PHASE_DATA_NOT_READY = 1,
   FP_NDS_F2_HTF_PHASE_NO_CANONICAL_F = 2,
   FP_NDS_F2_HTF_PHASE_HOOK_OR_ND = 3,
   FP_NDS_F2_HTF_PHASE_AMBIGUOUS = 4,
   FP_NDS_F2_HTF_PHASE_F_BULLISH = 5,
   FP_NDS_F2_HTF_PHASE_F_BEARISH = 6
};

struct FP_NDSF2HigherTimeframePhaseConfig
{
   bool enabled;
   ENUM_TIMEFRAMES timeframe;
   bool cancel_disallowed_pending_orders;

   int requested_bars;
   int min_closed_bars;
   int max_events;
   int max_hooks;

   bool use_multi_scale;
   int scale_l1;
   int scale_l2;
   int scale_l3;
   int scale_l4;
   int scale_l5;
   int scale_l6;
   int scale_l7;
   int scale_l8;

   double boundary_epsilon_points;
   double f2_min_parent_size_ratio;
   double f3_min_parent_size_ratio;
   double f3_leg1_L_min_ratio;
   double nd_min_retrace_ratio;
   bool nd_allow_below_half_cycle;
};

struct FP_NDSF2HigherTimeframePhaseSnapshot
{
   bool evaluated;
   bool gate_open;
   int state;
   int allowed_direction;

   string symbol;
   ENUM_TIMEFRAMES timeframe;
   datetime source_open_bar_time;
   datetime last_closed_bar_time;
   datetime refreshed_at;

   int copied_bars;
   int scale_count;
   int event_count;
   int hook_count;

   int selected_event_id;
   int selected_event_level;
   int selected_event_direction;
   int selected_event_scale_L;
   int selected_event_status;
   datetime selected_event_time;
   long selected_event_priority;

   int latest_hook_branch_id;
   int latest_hook_direction;
   int latest_hook_scale_L;
   datetime latest_hook_time;

   string reason;
};

void FP_ResetNDSF2HigherTimeframePhaseConfig(FP_NDSF2HigherTimeframePhaseConfig &cfg)
{
   cfg.enabled = true;
   cfg.timeframe = PERIOD_H1;
   cfg.cancel_disallowed_pending_orders = true;

   cfg.requested_bars = 900;
   cfg.min_closed_bars = 180;
   cfg.max_events = 2400;
   cfg.max_hooks = 2400;

   cfg.use_multi_scale = true;
   cfg.scale_l1 = 2;
   cfg.scale_l2 = 3;
   cfg.scale_l3 = 5;
   cfg.scale_l4 = 8;
   cfg.scale_l5 = 13;
   cfg.scale_l6 = 0;
   cfg.scale_l7 = 0;
   cfg.scale_l8 = 0;

   cfg.boundary_epsilon_points = 0.0;
   cfg.f2_min_parent_size_ratio = 1.0;
   cfg.f3_min_parent_size_ratio = 0.70;
   cfg.f3_leg1_L_min_ratio = 0.80;
   cfg.nd_min_retrace_ratio = 0.50;
   cfg.nd_allow_below_half_cycle = false;
}

void FP_ResetNDSF2HigherTimeframePhaseSnapshot(FP_NDSF2HigherTimeframePhaseSnapshot &s)
{
   s.evaluated = false;
   s.gate_open = false;
   s.state = FP_NDS_F2_HTF_PHASE_DATA_NOT_READY;
   s.allowed_direction = FP_DIR_NONE;

   s.symbol = "";
   s.timeframe = PERIOD_CURRENT;
   s.source_open_bar_time = 0;
   s.last_closed_bar_time = 0;
   s.refreshed_at = 0;

   s.copied_bars = 0;
   s.scale_count = 0;
   s.event_count = 0;
   s.hook_count = 0;

   s.selected_event_id = -1;
   s.selected_event_level = FP_LEVEL_NONE;
   s.selected_event_direction = FP_DIR_NONE;
   s.selected_event_scale_L = 0;
   s.selected_event_status = FP_STATUS_NONE;
   s.selected_event_time = 0;
   s.selected_event_priority = 0;

   s.latest_hook_branch_id = -1;
   s.latest_hook_direction = FP_DIR_NONE;
   s.latest_hook_scale_L = 0;
   s.latest_hook_time = 0;

   s.reason = "not_evaluated";
}

bool FP_NDSF2HTFDirectionIsValid(const int direction)
{
   return (direction == FP_DIR_BULLISH || direction == FP_DIR_BEARISH);
}

datetime FP_NDSF2HTFMaxTime(const datetime a, const datetime b)
{
   return (a > b ? a : b);
}

datetime FP_NDSF2HTFEventTime(const FP_FlagEvent &e)
{
   datetime t = 0;
   if(e.has_origin) t = FP_NDSF2HTFMaxTime(t, e.origin.time_anchor);
   if(e.has_leg1) t = FP_NDSF2HTFMaxTime(t, e.leg1.time_anchor);
   if(e.has_waist) t = FP_NDSF2HTFMaxTime(t, e.waist.time_anchor);
   if(e.has_leg2) t = FP_NDSF2HTFMaxTime(t, e.leg2.time_anchor);
   if(e.has_confirm) t = FP_NDSF2HTFMaxTime(t, e.confirm.time_anchor);
   if(e.has_extension) t = FP_NDSF2HTFMaxTime(t, e.extension_end.time_anchor);
   return t;
}

datetime FP_NDSF2HTFHookTime(const FP_HookBranch &h)
{
   datetime t = 0;
   t = FP_NDSF2HTFMaxTime(t, h.start_node.time_anchor);
   if(h.has_cycle_start) t = FP_NDSF2HTFMaxTime(t, h.cycle_start_node.time_anchor);
   t = FP_NDSF2HTFMaxTime(t, h.extreme_node.time_anchor);
   t = FP_NDSF2HTFMaxTime(t, h.resolve_node.time_anchor);
   t = FP_NDSF2HTFMaxTime(t, h.n1.time_anchor);
   t = FP_NDSF2HTFMaxTime(t, h.n2.time_anchor);
   t = FP_NDSF2HTFMaxTime(t, h.n3.time_anchor);
   t = FP_NDSF2HTFMaxTime(t, h.n4.time_anchor);
   return t;
}

bool FP_NDSF2HTFEventIsCanonicalFPhase(const FP_FlagEvent &e)
{
   if(!e.visible_main) return false;
   if(!FP_NDSF2HTFDirectionIsValid(e.direction)) return false;
   if(e.level != FP_LEVEL_F1 && e.level != FP_LEVEL_F2 && e.level != FP_LEVEL_F3)
      return false;
   if(e.status == FP_STATUS_INVALIDATED || e.body_status == FP_BODY_INVALID)
      return false;
   if(!e.has_origin || !e.has_leg1 || !e.has_waist || !e.has_leg2)
      return false;
   if(e.render_kind == FP_RENDER_NONE) return false;
   return (FP_NDSF2HTFEventTime(e) > 0);
}

bool FP_NDSF2HTFHookIsVisiblePhase(const FP_HookBranch &h)
{
   if(!h.visible_main) return false;
   if(!FP_NDSF2HTFDirectionIsValid(h.direction)) return false;
   if(h.status == FP_STATUS_INVALIDATED) return false;
   if(h.node_count < 3) return false;
   return (FP_NDSF2HTFHookTime(h) > 0);
}

long FP_NDSF2HTFEventPriority(const FP_FlagEvent &e)
{
   long p = 0;
   p += (long)MathMax(0, e.canonical_rank_final) * 1000000;
   p += (long)MathMax(0, e.owner_rank_score) * 1000;
   p += (long)MathMax(0, e.canonical_rank_score) * 10;
   p += (long)MathMax(0, e.level);
   return p;
}

bool FP_NDSF2HTFEventBeats(const FP_FlagEvent &candidate,
                           const datetime candidate_time,
                           const long candidate_priority,
                           const FP_FlagEvent &current,
                           const datetime current_time,
                           const long current_priority)
{
   if(candidate_time != current_time) return (candidate_time > current_time);
   if(candidate_priority != current_priority) return (candidate_priority > current_priority);
   if(candidate.level != current.level) return (candidate.level > current.level);
   if(candidate.scale_L != current.scale_L) return (candidate.scale_L > current.scale_L);
   return (candidate.event_id > current.event_id);
}

void FP_NDSF2HTFBuildDetectorConfig(const string symbol,
                                    const FP_NDSF2HigherTimeframePhaseConfig &src,
                                    FP_Config &cfg)
{
   FP_DefaultConfig(cfg);
   cfg.include_pending_nodes = false;
   cfg.scan_hooks = true;
   cfg.scan_f1 = true;
   cfg.scan_f2 = true;
   cfg.scan_f3 = true;
   cfg.show_invalidated_in_audit = false;
   cfg.keep_confirmed_f1f2_after_boundary_hit = false;

   // Higher-timeframe context must use the canonical ownership and Hook/ND
   // branch logic. It is deliberately not the relaxed F2 execution detector.
   cfg.require_f1_phase_boundary = true;
   cfg.allow_f1_fail_open_when_no_hook = true;
   cfg.strict_main_chart_ownership = true;
   cfg.ownership_hide_orphans = true;
   cfg.canonical_strict_invariants = true;
   cfg.canonical_hide_unresolved_orphans = true;
   cfg.hook_main_requires_visible_f1 = false;
   cfg.hook_keep_unseeded_visible_for_debug = true;

   cfg.f1_show_post_flag_candidates = true;
   cfg.f1_show_live_body_candidates = true;
   cfg.f2_show_size_rejected_candidates = true;
   cfg.f2_show_post_flag_candidates = true;
   cfg.f2_show_live_body_candidates = true;
   cfg.f3_show_or_rejected_candidates = true;
   cfg.f3_show_live_body_candidates = true;

   cfg.max_events = MathMax(100, src.max_events);
   cfg.max_hooks = MathMax(100, src.max_hooks);
   cfg.render_lookback_bars = 0;

   cfg.boundary_epsilon_points = src.boundary_epsilon_points;
   cfg.f2_min_parent_size_ratio = src.f2_min_parent_size_ratio;
   cfg.f3_min_parent_size_ratio = src.f3_min_parent_size_ratio;
   cfg.f3_leg1_L_min_ratio = src.f3_leg1_L_min_ratio;
   cfg.nd_min_retrace_ratio = src.nd_min_retrace_ratio;
   cfg.nd_allow_below_half_cycle = src.nd_allow_below_half_cycle;

   cfg.context_symbol = symbol;
   cfg.context_timeframe = EnumToString(src.timeframe);
   cfg.identity_generation_pass = "nds_f2_htf_f_phase_v1";
   cfg.identity_config_hash = "htf_f_phase_v1";
   cfg.verbose_logs = false;

   cfg.print_node_sanity = false;
   cfg.print_node_samples = false;
   cfg.print_identity_sanity = false;
   cfg.print_identity_samples = false;
   cfg.print_hook_sanity = false;
   cfg.print_hook_samples = false;
   cfg.print_body_sanity = false;
   cfg.print_body_samples = false;
   cfg.print_internal_sanity = false;
   cfg.print_internal_samples = false;
   cfg.print_f1_sanity = false;
   cfg.print_f1_samples = false;
   cfg.print_f2_sanity = false;
   cfg.print_f2_samples = false;
   cfg.print_f3_sanity = false;
   cfg.print_f3_samples = false;
   cfg.print_ownership_sanity = false;
   cfg.print_ownership_samples = false;
   cfg.print_canonical_sanity = false;
   cfg.print_canonical_samples = false;
}

int FP_NDSF2HTFBuildScales(const FP_NDSF2HigherTimeframePhaseConfig &cfg,
                           int &scales[])
{
   return FP_BuildScaleList(cfg.use_multi_scale,
                            cfg.scale_l1,
                            cfg.scale_l2,
                            cfg.scale_l3,
                            cfg.scale_l4,
                            cfg.scale_l5,
                            cfg.scale_l6,
                            cfg.scale_l7,
                            cfg.scale_l8,
                            scales);
}

bool FP_NDSF2RefreshHigherTimeframePhase(const string symbol,
                                         const FP_NDSF2HigherTimeframePhaseConfig &cfg,
                                         FP_NDSF2HigherTimeframePhaseSnapshot &snapshot)
{
   if(!cfg.enabled)
   {
      FP_ResetNDSF2HigherTimeframePhaseSnapshot(snapshot);
      snapshot.evaluated = true;
      snapshot.gate_open = true;
      snapshot.state = FP_NDS_F2_HTF_PHASE_DISABLED;
      snapshot.allowed_direction = FP_DIR_NONE;
      snapshot.symbol = symbol;
      snapshot.timeframe = cfg.timeframe;
      snapshot.reason = "higher_timeframe_filter_disabled";
      return true;
   }

   datetime open_bar = iTime(symbol, cfg.timeframe, 0);
   if(snapshot.evaluated &&
      snapshot.state != FP_NDS_F2_HTF_PHASE_DATA_NOT_READY &&
      snapshot.symbol == symbol &&
      snapshot.timeframe == cfg.timeframe &&
      snapshot.source_open_bar_time > 0 &&
      snapshot.source_open_bar_time == open_bar)
      return true;

   FP_ResetNDSF2HigherTimeframePhaseSnapshot(snapshot);
   snapshot.symbol = symbol;
   snapshot.timeframe = cfg.timeframe;
   snapshot.source_open_bar_time = open_bar;
   snapshot.refreshed_at = TimeCurrent();

   if(open_bar <= 0)
   {
      snapshot.evaluated = true;
      snapshot.reason = "higher_timeframe_open_bar_unavailable";
      return false;
   }

   FP_TimebaseConfig timebase_cfg;
   FP_DefaultTimebaseConfig(timebase_cfg);
   timebase_cfg.symbol = symbol;
   timebase_cfg.period = cfg.timeframe;
   timebase_cfg.requested_bars = MathMax(cfg.min_closed_bars, cfg.requested_bars);
   timebase_cfg.min_closed_bars = MathMax(50, cfg.min_closed_bars);
   timebase_cfg.exclude_live_bar = true;
   timebase_cfg.require_ascending_time = true;
   timebase_cfg.strict_contract = true;
   timebase_cfg.print_sanity = false;
   timebase_cfg.print_samples = false;

   MqlRates rates[];
   FP_TimebaseReport timebase_report;
   int copied = FP_LoadCanonicalRates(timebase_cfg, rates, timebase_report);
   snapshot.copied_bars = copied;
   if(copied > 0) snapshot.last_closed_bar_time = rates[copied - 1].time;
   if(!timebase_report.ok || copied < timebase_cfg.min_closed_bars)
   {
      snapshot.evaluated = true;
      snapshot.state = FP_NDS_F2_HTF_PHASE_DATA_NOT_READY;
      snapshot.reason = "higher_timeframe_closed_history_not_ready";
      return false;
   }

   int scales[];
   int scale_count = FP_NDSF2HTFBuildScales(cfg, scales);
   snapshot.scale_count = scale_count;
   if(scale_count <= 0)
   {
      snapshot.evaluated = true;
      snapshot.state = FP_NDS_F2_HTF_PHASE_DATA_NOT_READY;
      snapshot.reason = "higher_timeframe_scale_list_empty";
      return false;
   }

   FP_Config detector_cfg;
   FP_NDSF2HTFBuildDetectorConfig(symbol, cfg, detector_cfg);

   FP_FlagEvent events[];
   FP_HookBranch hooks[];
   FP_DetectResult detect_result;
   FP_DetectAllScales(rates, copied, scales, scale_count,
                      detector_cfg, events, hooks, detect_result);
   snapshot.event_count = ArraySize(events);
   snapshot.hook_count = ArraySize(hooks);

   int best = -1;
   datetime best_time = 0;
   long best_priority = 0;
   bool top_direction_conflict = false;

   for(int i=0; i<ArraySize(events); i++)
   {
      if(!FP_NDSF2HTFEventIsCanonicalFPhase(events[i])) continue;
      datetime event_time = FP_NDSF2HTFEventTime(events[i]);
      long priority = FP_NDSF2HTFEventPriority(events[i]);
      if(best < 0 || FP_NDSF2HTFEventBeats(events[i], event_time, priority,
                                           events[best], best_time, best_priority))
      {
         best = i;
         best_time = event_time;
         best_priority = priority;
         top_direction_conflict = false;
      }
      else if(best >= 0 && event_time == best_time && priority == best_priority &&
              events[i].direction != events[best].direction)
      {
         top_direction_conflict = true;
      }
   }

   datetime latest_hook_time = 0;
   int latest_hook = -1;
   for(int i=0; i<ArraySize(hooks); i++)
   {
      if(!FP_NDSF2HTFHookIsVisiblePhase(hooks[i])) continue;
      datetime hook_time = FP_NDSF2HTFHookTime(hooks[i]);
      if(latest_hook < 0 || hook_time > latest_hook_time ||
         (hook_time == latest_hook_time && hooks[i].scale_L > hooks[latest_hook].scale_L))
      {
         latest_hook = i;
         latest_hook_time = hook_time;
      }
   }

   snapshot.evaluated = true;
   if(latest_hook >= 0)
   {
      snapshot.latest_hook_branch_id = hooks[latest_hook].branch_id;
      snapshot.latest_hook_direction = hooks[latest_hook].direction;
      snapshot.latest_hook_scale_L = hooks[latest_hook].scale_L;
      snapshot.latest_hook_time = latest_hook_time;
   }

   if(best < 0)
   {
      snapshot.state = FP_NDS_F2_HTF_PHASE_NO_CANONICAL_F;
      snapshot.reason = "no_visible_canonical_higher_timeframe_f";
      return true;
   }

   snapshot.selected_event_id = events[best].event_id;
   snapshot.selected_event_level = events[best].level;
   snapshot.selected_event_direction = events[best].direction;
   snapshot.selected_event_scale_L = events[best].scale_L;
   snapshot.selected_event_status = events[best].status;
   snapshot.selected_event_time = best_time;
   snapshot.selected_event_priority = best_priority;

   if(top_direction_conflict)
   {
      snapshot.state = FP_NDS_F2_HTF_PHASE_AMBIGUOUS;
      snapshot.reason = "equal_priority_opposite_higher_timeframe_f_events";
      return true;
   }

   // A Hook/ND context at or after the most recent canonical F endpoint owns the
   // current higher-timeframe phase. Entry is fail-closed until a newer F event
   // reclaims phase authority.
   if(latest_hook >= 0 && latest_hook_time >= best_time)
   {
      snapshot.state = FP_NDS_F2_HTF_PHASE_HOOK_OR_ND;
      snapshot.reason = "latest_higher_timeframe_context_is_hook_or_nd";
      return true;
   }

   snapshot.allowed_direction = events[best].direction;
   snapshot.gate_open = FP_NDSF2HTFDirectionIsValid(snapshot.allowed_direction);
   snapshot.state = (snapshot.allowed_direction == FP_DIR_BULLISH
                     ? FP_NDS_F2_HTF_PHASE_F_BULLISH
                     : FP_NDS_F2_HTF_PHASE_F_BEARISH);
   snapshot.reason = (snapshot.allowed_direction == FP_DIR_BULLISH
                      ? "higher_timeframe_canonical_f_bullish"
                      : "higher_timeframe_canonical_f_bearish");
   return true;
}

bool FP_NDSF2HigherTimeframeAllowsDirection(
   const FP_NDSF2HigherTimeframePhaseConfig &cfg,
   const FP_NDSF2HigherTimeframePhaseSnapshot &snapshot,
   const int direction)
{
   if(!cfg.enabled) return true;
   if(!snapshot.evaluated || !snapshot.gate_open) return false;
   return (direction == snapshot.allowed_direction);
}

#endif // __FP_NDS_F2_HIGHER_TIMEFRAME_PHASE_FILTER_MQH__
