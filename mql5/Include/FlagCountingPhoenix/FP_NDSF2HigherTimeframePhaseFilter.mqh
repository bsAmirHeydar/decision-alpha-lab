#ifndef __FP_NDS_F2_HIGHER_TIMEFRAME_PHASE_FILTER_MQH__
#define __FP_NDS_F2_HIGHER_TIMEFRAME_PHASE_FILTER_MQH__
#property strict

#include "FP_Timebase.mqh"
#include "FP_NodeScaleList.mqh"
#include "FP_SequenceEngine.mqh"

#define FP_NDS_F2_HTF_PHASE_FILTER_VERSION "NDS-F2-HTF-F-PHASE-03"

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

enum FP_NDSF2HigherTimeframeF1F2WindowState
{
   FP_NDS_F2_HTF_F1_F2_WINDOW_DISABLED = 0,
   FP_NDS_F2_HTF_F1_F2_WINDOW_NOT_EVALUATED = 1,
   FP_NDS_F2_HTF_F1_F2_WINDOW_SEQUENCE_MISSING = 2,
   FP_NDS_F2_HTF_F1_F2_WINDOW_AMBIGUOUS = 3,
   FP_NDS_F2_HTF_F1_F2_WINDOW_BEFORE_F1_CONFIRM = 4,
   FP_NDS_F2_HTF_F1_F2_WINDOW_OPEN = 5,
   FP_NDS_F2_HTF_F1_F2_WINDOW_CLOSED_AFTER_F2_CONFIRM = 6
};

struct FP_NDSF2HigherTimeframePhaseConfig
{
   bool enabled;
   ENUM_TIMEFRAMES timeframe;
   bool require_f1_confirmed_before_f2_confirmed_window;
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

   bool f1_to_f2_window_evaluated;
   bool f1_to_f2_window_open;
   int f1_to_f2_window_state;
   int selected_sequence_id;
   int selected_f1_event_id;
   int selected_f1_status;
   int selected_f1_lifecycle_status;
   datetime selected_f1_confirm_time;
   int selected_f2_event_id;
   int selected_f2_status;
   int selected_f2_lifecycle_status;
   datetime selected_f2_confirm_time;

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

   int evaluated_count_total;
   int qualifying_count_total;
   int qualifying_bullish_count;
   int qualifying_bearish_count;
   int same_count_hook_blocked_total;
   int before_f1_total;
   int after_f2_total;
   int ambiguous_count_total;

   string reason;
};

struct FP_NDSF2HTFCountEvaluation
{
   bool evaluated;
   bool qualifies;
   int direction;
   int sequence_id;
   int f1_index;
   int f2_index;
   int latest_event_index;
   int window_state;
   bool hook_blocked;
   int hook_index;
   datetime latest_event_time;
   long latest_event_priority;
};

void FP_ResetNDSF2HigherTimeframePhaseConfig(FP_NDSF2HigherTimeframePhaseConfig &cfg)
{
   cfg.enabled = true;
   cfg.timeframe = PERIOD_H1;
   cfg.require_f1_confirmed_before_f2_confirmed_window = true;
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
   s.f1_to_f2_window_evaluated = false;
   s.f1_to_f2_window_open = false;
   s.f1_to_f2_window_state = FP_NDS_F2_HTF_F1_F2_WINDOW_NOT_EVALUATED;
   s.selected_sequence_id = -1;
   s.selected_f1_event_id = -1;
   s.selected_f1_status = FP_STATUS_NONE;
   s.selected_f1_lifecycle_status = FP_F1_LC_NONE;
   s.selected_f1_confirm_time = 0;
   s.selected_f2_event_id = -1;
   s.selected_f2_status = FP_STATUS_NONE;
   s.selected_f2_lifecycle_status = FP_F2_LC_NONE;
   s.selected_f2_confirm_time = 0;
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
   s.evaluated_count_total = 0;
   s.qualifying_count_total = 0;
   s.qualifying_bullish_count = 0;
   s.qualifying_bearish_count = 0;
   s.same_count_hook_blocked_total = 0;
   s.before_f1_total = 0;
   s.after_f2_total = 0;
   s.ambiguous_count_total = 0;
   s.reason = "not_evaluated";
}

void FP_ResetNDSF2HTFCountEvaluation(FP_NDSF2HTFCountEvaluation &e)
{
   e.evaluated = false;
   e.qualifies = false;
   e.direction = FP_DIR_NONE;
   e.sequence_id = -1;
   e.f1_index = -1;
   e.f2_index = -1;
   e.latest_event_index = -1;
   e.window_state = FP_NDS_F2_HTF_F1_F2_WINDOW_NOT_EVALUATED;
   e.hook_blocked = false;
   e.hook_index = -1;
   e.latest_event_time = 0;
   e.latest_event_priority = 0;
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

bool FP_NDSF2HTFIsConfirmedF1(const FP_FlagEvent &e)
{
   return (e.level == FP_LEVEL_F1 &&
           e.chain_index == 1 &&
           e.status == FP_STATUS_CONFIRMED &&
           e.lifecycle_status == FP_F1_LC_CONFIRMED &&
           e.has_confirm);
}

bool FP_NDSF2HTFIsConfirmedF2(const FP_FlagEvent &e)
{
   return (e.level == FP_LEVEL_F2 &&
           e.chain_index == 2 &&
           e.status == FP_STATUS_CONFIRMED &&
           e.f2_lifecycle_status == FP_F2_LC_CONFIRMED &&
           e.has_confirm);
}

bool FP_NDSF2HTFEventBelongsToRoot(const FP_FlagEvent &e,
                                   const FP_FlagEvent &f1)
{
   return (e.sequence_id == f1.sequence_id &&
           e.direction == f1.direction &&
           e.scale_L == f1.scale_L);
}

int FP_NDSF2HTFHookOwnerRootIndex(const FP_HookBranch &h,
                                   const FP_FlagEvent &events[],
                                   const double eps)
{
   if(!FP_NDSF2HTFHookIsVisiblePhase(h)) return -1;
   FP_Node hook_origin = FP_HookOriginNode(h, eps);

   // Exact seed ownership has first authority.
   if(hook_origin.id >= 0)
   {
      for(int i=0; i<ArraySize(events); i++)
      {
         if(events[i].level != FP_LEVEL_F1 || events[i].chain_index != 1) continue;
         if(!FP_NDSF2HTFEventIsCanonicalFPhase(events[i])) continue;
         if(events[i].direction != h.direction || events[i].scale_L != h.scale_L) continue;
         if(!events[i].has_origin) continue;
         if(events[i].origin.kind != hook_origin.kind) continue;
         if(events[i].origin.index_anchor != hook_origin.index_anchor) continue;
         if(!FP_AlmostEqual(events[i].origin.price, hook_origin.price, eps)) continue;
         return i;
      }
   }

   // A later Hook/ND transition belongs to the most recent canonical root on
   // the same direction and scale whose origin precedes that Hook. This keeps
   // Hook veto local to one count instead of allowing an unrelated scale/count
   // to close the entire higher-timeframe gate.
   int hook_start = (h.has_cycle_start
                     ? h.cycle_start_node.index_anchor
                     : h.start_node.index_anchor);
   int best = -1;
   int best_origin = -1;
   for(int i=0; i<ArraySize(events); i++)
   {
      if(events[i].level != FP_LEVEL_F1 || events[i].chain_index != 1) continue;
      if(!FP_NDSF2HTFEventIsCanonicalFPhase(events[i])) continue;
      if(events[i].direction != h.direction || events[i].scale_L != h.scale_L) continue;
      if(!events[i].has_origin || events[i].origin.index_anchor > hook_start) continue;
      if(best < 0 || events[i].origin.index_anchor > best_origin)
      {
         best = i;
         best_origin = events[i].origin.index_anchor;
      }
   }
   return best;
}

bool FP_NDSF2HTFHookBelongsToRoot(const FP_HookBranch &h,
                                  const FP_FlagEvent &events[],
                                  const FP_FlagEvent &f1,
                                  const double eps)
{
   int owner = FP_NDSF2HTFHookOwnerRootIndex(h, events, eps);
   if(owner < 0) return false;
   return (events[owner].sequence_id == f1.sequence_id);
}

int FP_NDSF2HTFFindLatestSequenceEvent(const FP_FlagEvent &events[],
                                       const FP_FlagEvent &f1)
{
   int best = -1;
   datetime best_time = 0;
   long best_priority = 0;
   for(int i=0; i<ArraySize(events); i++)
   {
      if(!FP_NDSF2HTFEventBelongsToRoot(events[i], f1)) continue;
      if(!FP_NDSF2HTFEventIsCanonicalFPhase(events[i])) continue;
      datetime t = FP_NDSF2HTFEventTime(events[i]);
      long p = FP_NDSF2HTFEventPriority(events[i]);
      if(best < 0 || FP_NDSF2HTFEventBeats(events[i], t, p,
                                           events[best], best_time, best_priority))
      {
         best = i;
         best_time = t;
         best_priority = p;
      }
   }
   return best;
}

int FP_NDSF2HTFFindDirectChildF2(const FP_FlagEvent &events[],
                                 const FP_FlagEvent &f1)
{
   int best = -1;
   datetime best_time = 0;
   long best_priority = 0;
   for(int i=0; i<ArraySize(events); i++)
   {
      FP_FlagEvent e = events[i];
      if(e.level != FP_LEVEL_F2 || e.chain_index != 2) continue;
      if(!FP_NDSF2HTFEventBelongsToRoot(e, f1)) continue;
      if(e.parent_sequence_id != f1.sequence_id || e.parent_event_id != f1.event_id)
         continue;
      datetime t = FP_NDSF2HTFEventTime(e);
      long p = FP_NDSF2HTFEventPriority(e);
      if(best < 0 || FP_NDSF2HTFEventBeats(e, t, p,
                                           events[best], best_time, best_priority))
      {
         best = i;
         best_time = t;
         best_priority = p;
      }
   }
   return best;
}

bool FP_NDSF2HTFEvaluateCount(const FP_FlagEvent &events[],
                              const FP_HookBranch &hooks[],
                              const int f1_index,
                              const FP_NDSF2HigherTimeframePhaseConfig &cfg,
                              FP_NDSF2HTFCountEvaluation &out)
{
   FP_ResetNDSF2HTFCountEvaluation(out);
   out.evaluated = true;
   if(f1_index < 0 || f1_index >= ArraySize(events))
   {
      out.window_state = FP_NDS_F2_HTF_F1_F2_WINDOW_SEQUENCE_MISSING;
      return false;
   }

   FP_FlagEvent f1 = events[f1_index];
   out.f1_index = f1_index;
   out.direction = f1.direction;
   out.sequence_id = f1.sequence_id;
   if(f1.level != FP_LEVEL_F1 || f1.chain_index != 1 ||
      !FP_NDSF2HTFEventIsCanonicalFPhase(f1) || f1.sequence_id < 0)
   {
      out.window_state = FP_NDS_F2_HTF_F1_F2_WINDOW_SEQUENCE_MISSING;
      return false;
   }

   out.latest_event_index = FP_NDSF2HTFFindLatestSequenceEvent(events, f1);
   if(out.latest_event_index < 0)
   {
      out.window_state = FP_NDS_F2_HTF_F1_F2_WINDOW_SEQUENCE_MISSING;
      return false;
   }
   out.latest_event_time = FP_NDSF2HTFEventTime(events[out.latest_event_index]);
   out.latest_event_priority = FP_NDSF2HTFEventPriority(events[out.latest_event_index]);

   double eps = FP_EpsilonPrice(cfg.boundary_epsilon_points);
   datetime latest_matching_hook_time = 0;
   for(int i=0; i<ArraySize(hooks); i++)
   {
      if(!FP_NDSF2HTFHookBelongsToRoot(hooks[i], events, f1, eps)) continue;
      datetime t = FP_NDSF2HTFHookTime(hooks[i]);
      if(out.hook_index < 0 || t > latest_matching_hook_time)
      {
         out.hook_index = i;
         latest_matching_hook_time = t;
      }
   }
   if(out.hook_index >= 0 && latest_matching_hook_time >= out.latest_event_time)
   {
      out.hook_blocked = true;
      out.window_state = FP_NDS_F2_HTF_F1_F2_WINDOW_NOT_EVALUATED;
      return true;
   }

   if(!cfg.require_f1_confirmed_before_f2_confirmed_window)
   {
      out.window_state = FP_NDS_F2_HTF_F1_F2_WINDOW_DISABLED;
      out.qualifies = true;
      return true;
   }

   if(!FP_NDSF2HTFIsConfirmedF1(f1))
   {
      out.window_state = FP_NDS_F2_HTF_F1_F2_WINDOW_BEFORE_F1_CONFIRM;
      return true;
   }

   out.f2_index = FP_NDSF2HTFFindDirectChildF2(events, f1);
   if(out.f2_index >= 0 && FP_NDSF2HTFIsConfirmedF2(events[out.f2_index]))
   {
      out.window_state = FP_NDS_F2_HTF_F1_F2_WINDOW_CLOSED_AFTER_F2_CONFIRM;
      return true;
   }

   out.window_state = FP_NDS_F2_HTF_F1_F2_WINDOW_OPEN;
   out.qualifies = true;
   return true;
}

void FP_NDSF2HTFCopySelectedCount(const FP_FlagEvent &events[],
                                  const FP_HookBranch &hooks[],
                                  const FP_NDSF2HTFCountEvaluation &e,
                                  FP_NDSF2HigherTimeframePhaseSnapshot &snapshot)
{
   snapshot.selected_sequence_id = e.sequence_id;
   snapshot.f1_to_f2_window_evaluated = true;
   snapshot.f1_to_f2_window_open = e.qualifies;
   snapshot.f1_to_f2_window_state = e.window_state;

   if(e.f1_index >= 0 && e.f1_index < ArraySize(events))
   {
      FP_FlagEvent f1 = events[e.f1_index];
      snapshot.selected_f1_event_id = f1.event_id;
      snapshot.selected_f1_status = f1.status;
      snapshot.selected_f1_lifecycle_status = f1.lifecycle_status;
      snapshot.selected_f1_confirm_time = (f1.has_confirm ? f1.confirm.time_anchor : 0);
   }
   if(e.f2_index >= 0 && e.f2_index < ArraySize(events))
   {
      FP_FlagEvent f2 = events[e.f2_index];
      snapshot.selected_f2_event_id = f2.event_id;
      snapshot.selected_f2_status = f2.status;
      snapshot.selected_f2_lifecycle_status = f2.f2_lifecycle_status;
      snapshot.selected_f2_confirm_time = (f2.has_confirm ? f2.confirm.time_anchor : 0);
   }
   if(e.latest_event_index >= 0 && e.latest_event_index < ArraySize(events))
   {
      FP_FlagEvent selected = events[e.latest_event_index];
      snapshot.selected_event_id = selected.event_id;
      snapshot.selected_event_level = selected.level;
      snapshot.selected_event_direction = selected.direction;
      snapshot.selected_event_scale_L = selected.scale_L;
      snapshot.selected_event_status = selected.status;
      snapshot.selected_event_time = e.latest_event_time;
      snapshot.selected_event_priority = e.latest_event_priority;
   }
   if(e.hook_index >= 0 && e.hook_index < ArraySize(hooks))
   {
      FP_HookBranch h = hooks[e.hook_index];
      snapshot.latest_hook_branch_id = h.branch_id;
      snapshot.latest_hook_direction = h.direction;
      snapshot.latest_hook_scale_L = h.scale_L;
      snapshot.latest_hook_time = FP_NDSF2HTFHookTime(h);
   }
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
   cfg.identity_generation_pass = "nds_f2_htf_f_phase_v3";
   cfg.identity_config_hash = "htf_f_phase_v3";
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
                            cfg.scale_l1, cfg.scale_l2, cfg.scale_l3, cfg.scale_l4,
                            cfg.scale_l5, cfg.scale_l6, cfg.scale_l7, cfg.scale_l8,
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
      snapshot.f1_to_f2_window_evaluated = true;
      snapshot.f1_to_f2_window_open = true;
      snapshot.f1_to_f2_window_state = FP_NDS_F2_HTF_F1_F2_WINDOW_DISABLED;
      snapshot.symbol = symbol;
      snapshot.timeframe = cfg.timeframe;
      snapshot.reason = "higher_timeframe_filter_disabled";
      return true;
   }

   datetime open_bar = iTime(symbol, cfg.timeframe, 0);
   if(snapshot.evaluated &&
      snapshot.state != FP_NDS_F2_HTF_PHASE_DATA_NOT_READY &&
      snapshot.symbol == symbol && snapshot.timeframe == cfg.timeframe &&
      snapshot.source_open_bar_time > 0 && snapshot.source_open_bar_time == open_bar)
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
   snapshot.evaluated = true;

   FP_NDSF2HTFCountEvaluation best_bull;
   FP_NDSF2HTFCountEvaluation best_bear;
   FP_ResetNDSF2HTFCountEvaluation(best_bull);
   FP_ResetNDSF2HTFCountEvaluation(best_bear);

   int seen_sequences[];
   ArrayResize(seen_sequences, 0);
   for(int i=0; i<ArraySize(events); i++)
   {
      if(events[i].level != FP_LEVEL_F1 || events[i].chain_index != 1) continue;
      if(!FP_NDSF2HTFEventIsCanonicalFPhase(events[i])) continue;

      bool seen = false;
      for(int k=0; k<ArraySize(seen_sequences); k++)
         if(seen_sequences[k] == events[i].sequence_id) { seen = true; break; }
      if(seen) continue;
      int sn = ArraySize(seen_sequences);
      if(ArrayResize(seen_sequences, sn + 1) != sn + 1) break;
      seen_sequences[sn] = events[i].sequence_id;

      FP_NDSF2HTFCountEvaluation eval;
      FP_NDSF2HTFEvaluateCount(events, hooks, i, cfg, eval);
      snapshot.evaluated_count_total++;
      if(eval.hook_blocked) snapshot.same_count_hook_blocked_total++;
      if(eval.window_state == FP_NDS_F2_HTF_F1_F2_WINDOW_BEFORE_F1_CONFIRM)
         snapshot.before_f1_total++;
      if(eval.window_state == FP_NDS_F2_HTF_F1_F2_WINDOW_CLOSED_AFTER_F2_CONFIRM)
         snapshot.after_f2_total++;
      if(eval.window_state == FP_NDS_F2_HTF_F1_F2_WINDOW_AMBIGUOUS)
         snapshot.ambiguous_count_total++;
      if(!eval.qualifies) continue;

      snapshot.qualifying_count_total++;
      if(eval.direction == FP_DIR_BULLISH)
      {
         snapshot.qualifying_bullish_count++;
         if(!best_bull.qualifies || eval.latest_event_time > best_bull.latest_event_time ||
            (eval.latest_event_time == best_bull.latest_event_time &&
             eval.latest_event_priority > best_bull.latest_event_priority))
            best_bull = eval;
      }
      else if(eval.direction == FP_DIR_BEARISH)
      {
         snapshot.qualifying_bearish_count++;
         if(!best_bear.qualifies || eval.latest_event_time > best_bear.latest_event_time ||
            (eval.latest_event_time == best_bear.latest_event_time &&
             eval.latest_event_priority > best_bear.latest_event_priority))
            best_bear = eval;
      }
   }

   if(snapshot.qualifying_bullish_count > 0 && snapshot.qualifying_bearish_count > 0)
   {
      snapshot.state = FP_NDS_F2_HTF_PHASE_AMBIGUOUS;
      snapshot.reason = "opposite_direction_qualifying_higher_timeframe_counts";
      return true;
   }

   FP_NDSF2HTFCountEvaluation selected;
   FP_ResetNDSF2HTFCountEvaluation(selected);
   if(snapshot.qualifying_bullish_count > 0) selected = best_bull;
   else if(snapshot.qualifying_bearish_count > 0) selected = best_bear;

   if(selected.qualifies)
   {
      FP_NDSF2HTFCopySelectedCount(events, hooks, selected, snapshot);
      snapshot.allowed_direction = selected.direction;
      snapshot.state = (selected.direction == FP_DIR_BULLISH
                        ? FP_NDS_F2_HTF_PHASE_F_BULLISH
                        : FP_NDS_F2_HTF_PHASE_F_BEARISH);
      snapshot.gate_open = true;
      snapshot.reason = (selected.direction == FP_DIR_BULLISH
                         ? "qualifying_bullish_count_in_f_phase"
                         : "qualifying_bearish_count_in_f_phase");
      return true;
   }

   snapshot.gate_open = false;
   if(snapshot.evaluated_count_total <= 0)
   {
      snapshot.state = FP_NDS_F2_HTF_PHASE_NO_CANONICAL_F;
      snapshot.reason = "no_visible_canonical_higher_timeframe_f_count";
   }
   else if(snapshot.same_count_hook_blocked_total > 0 &&
           snapshot.same_count_hook_blocked_total == snapshot.evaluated_count_total)
   {
      snapshot.state = FP_NDS_F2_HTF_PHASE_HOOK_OR_ND;
      snapshot.reason = "all_higher_timeframe_counts_owned_by_their_own_hook_or_nd";
   }
   else
   {
      snapshot.state = FP_NDS_F2_HTF_PHASE_NO_CANONICAL_F;
      snapshot.reason = "no_higher_timeframe_count_inside_requested_f1_to_f2_window";
   }
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
