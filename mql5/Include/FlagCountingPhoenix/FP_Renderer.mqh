#ifndef __FP_RENDERER_MQH__
#define __FP_RENDERER_MQH__
#property strict

#include "FP_RenderAudit.mqh"

// ============================================================================
// Phoenix Level 12 - Renderer / Labels / Visual Layer
// ----------------------------------------------------------------------------
// Renderer is non-authoritative. It draws only emitted canonical events/hooks.
// It never creates, hides, promotes, confirms, locks, invalidates, repairs, or
// infers market structure by itself.
// ============================================================================

int FP_DeleteObjectsByPrefix(const string prefix)
{
   int total = ObjectsTotal(0, -1, -1);
   int deleted = 0;
   for(int i=total-1; i>=0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(StringFind(name, prefix) == 0)
      {
         if(ObjectDelete(0, name)) deleted++;
      }
   }
   return deleted;
}

color FP_StatusColor(const FP_FlagEvent &e,
                     const color bull_candidate,
                     const color bull_confirmed,
                     const color bear_candidate,
                     const color bear_confirmed,
                     const color f3_locked)
{
   if(e.level == FP_LEVEL_F3 && e.status == FP_STATUS_LOCKED) return f3_locked;
   if(e.direction == FP_DIR_BULLISH)
   {
      if(e.status == FP_STATUS_CONFIRMED || e.status == FP_STATUS_COMPLETED || e.status == FP_STATUS_LOCKED) return bull_confirmed;
      return bull_candidate;
   }
   if(e.direction == FP_DIR_BEARISH)
   {
      if(e.status == FP_STATUS_CONFIRMED || e.status == FP_STATUS_COMPLETED || e.status == FP_STATUS_LOCKED) return bear_confirmed;
      return bear_candidate;
   }
   return clrSilver;
}

color FP_ShadeColor(const color c, const int event_id, const bool use_shades)
{
   if(!use_shades) return c;
   int r = (int)(c & 0x0000FF);
   int g = (int)((c & 0x00FF00) >> 8);
   int b = (int)((c & 0xFF0000) >> 16);
   int delta = (event_id % 5) * 12;
   r = MathMin(255, MathMax(0, r + delta));
   g = MathMin(255, MathMax(0, g + delta));
   b = MathMin(255, MathMax(0, b + delta));
   return (color)(r | (g << 8) | (b << 16));
}

bool FP_CreateTrend(const string name,
                    const datetime t1,
                    const double p1,
                    const datetime t2,
                    const double p2,
                    const color c,
                    const int width,
                    const ENUM_LINE_STYLE style,
                    const bool draw_back,
                    FP_RenderReport &report)
{
   report.objects_requested++;
   if(ObjectFind(0, name) >= 0)
   {
      report.duplicate_object_names++;
      ObjectDelete(0, name);
   }
   if(!ObjectCreate(0, name, OBJ_TREND, 0, t1, p1, t2, p2))
   {
      report.object_create_failures++;
      report.ok = false;
      report.reason = "object_create_failed";
      return false;
   }
   report.objects_created++;
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, false);
   ObjectSetInteger(0, name, OBJPROP_RAY_LEFT, false);
   ObjectSetInteger(0, name, OBJPROP_BACK, draw_back);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTED, false);
   return true;
}

bool FP_CreateText(const string name,
                   const datetime t,
                   const double p,
                   const string text,
                   const color c,
                   const int font_size,
                   FP_RenderReport &report)
{
   report.objects_requested++;
   if(ObjectFind(0, name) >= 0)
   {
      report.duplicate_object_names++;
      ObjectDelete(0, name);
   }
   if(!ObjectCreate(0, name, OBJ_TEXT, 0, t, p))
   {
      report.object_create_failures++;
      report.ok = false;
      report.reason = "object_create_failed";
      return false;
   }
   report.objects_created++;
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, MathMax(7, font_size));
   ObjectSetString(0, name, OBJPROP_FONT, "Arial");
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTED, false);
   return true;
}

string FP_EventLabel(const FP_FlagEvent &e, const bool detailed, const bool show_parent)
{
   string s = FP_LevelName(e.level) + " L" + IntegerToString(e.scale_L) + " Q" + IntegerToString(e.event_id);
   if(show_parent && e.parent_event_id >= 0) s = s + " P" + IntegerToString(e.parent_event_id);
   s = s + " " + FP_StatusName(e.status);
   if(detailed)
   {
      if(StringLen(e.canonical_id) > 0) s = s + " C" + FP_RenderSafeId(e.canonical_id, 12);
      if(StringLen(e.chain_id) > 0) s = s + " CH" + FP_RenderSafeId(e.chain_id, 10);
      s = s + " O" + IntegerToString(e.origin.id);
      if(e.has_leg1) s = s + " A" + IntegerToString(e.leg1.id);
      if(e.has_waist) s = s + " W" + IntegerToString(e.waist.id);
      if(e.has_leg2) s = s + " B" + IntegerToString(e.leg2.id);
      if(e.level == FP_LEVEL_F2)
      {
         s = s + " sz" + FP_BoolName(e.f2_size_gate_passed);
      }
      if(e.level == FP_LEVEL_F3)
      {
         s = s + " OR" + FP_BoolName(e.f3_or_gate_passed);
         if(e.f3_locked) s = s + " lockQ" + IntegerToString(e.f3_lock_event_id);
      }
      if(StringLen(e.hidden_reason) > 0 && !e.visible_main) s = s + " H" + FP_RenderSafeId(e.hidden_reason, 10);
   }
   return s;
}

double FP_LabelStepPrice()
{
   double point_floor = 80.0 * _Point;
   if(_Digits == 3 || _Digits == 5) point_floor = 800.0 * _Point;

   double pmax = 0.0;
   double pmin = 0.0;
   bool got_max = ChartGetDouble(0, CHART_PRICE_MAX, 0, pmax);
   bool got_min = ChartGetDouble(0, CHART_PRICE_MIN, 0, pmin);
   if(got_max && got_min && pmax > pmin)
   {
      double viewport_step = (pmax - pmin) * 0.018;
      return MathMax(point_floor, viewport_step);
   }
   return point_floor;
}

double FP_LabelOffsetPrice(const int lane, const bool is_peak)
{
   double sign = (is_peak ? 1.0 : -1.0);
   return sign * (double)(lane + 1) * FP_LabelStepPrice();
}

struct FP_LabelStackCluster
{
   int index_anchor;
   datetime time_anchor;
   double price_anchor;
   bool is_peak;
   int used_lanes;
};

int FP_LabelTimeClusterBars()
{
   return 18;
}

double FP_LabelPriceClusterDistance()
{
   return FP_LabelStepPrice() * 6.0;
}

int FP_RegisterLabelCluster(FP_LabelStackCluster &clusters[],
                            const int index_anchor,
                            const datetime time_anchor,
                            const double price,
                            const bool is_peak,
                            datetime &out_time_anchor,
                            double &out_price_anchor)
{
   int n = ArraySize(clusters);
   int best = -1;
   int best_dt = 1000000000;
   double price_cluster = FP_LabelPriceClusterDistance();
   int time_cluster_bars = FP_LabelTimeClusterBars();

   for(int i=0; i<n; i++)
   {
      if(clusters[i].is_peak != is_peak) continue;
      int dt = MathAbs(clusters[i].index_anchor - index_anchor);
      if(dt > time_cluster_bars) continue;
      if(MathAbs(clusters[i].price_anchor - price) > price_cluster) continue;
      if(dt < best_dt)
      {
         best = i;
         best_dt = dt;
      }
   }

   if(best >= 0)
   {
      int lane = clusters[best].used_lanes;
      clusters[best].used_lanes = clusters[best].used_lanes + 1;
      out_time_anchor = clusters[best].time_anchor;
      out_price_anchor = clusters[best].price_anchor;
      return lane;
   }

   ArrayResize(clusters, n + 1);
   clusters[n].index_anchor = index_anchor;
   clusters[n].time_anchor = time_anchor;
   clusters[n].price_anchor = price;
   clusters[n].is_peak = is_peak;
   clusters[n].used_lanes = 1;
   out_time_anchor = time_anchor;
   out_price_anchor = price;
   return 0;
}

datetime FP_TimeAtIndex(const MqlRates &rates[], const int rates_total, const int index_anchor, const datetime fallback_time)
{
   if(index_anchor >= 0 && index_anchor < rates_total)
      return rates[index_anchor].time;
   return fallback_time;
}

int FP_NormalizeIndex(const int index_anchor, const int rates_total)
{
   if(index_anchor < 0) return -1;
   if(index_anchor >= rates_total) return -1;
   return index_anchor;
}

bool FP_DrawIndexSampledArcR(const string base,
                             const FP_Node &start,
                             const FP_Node &control,
                             const FP_Node &finish,
                             const MqlRates &rates[],
                             const int rates_total,
                             const color c,
                             const int width,
                             const ENUM_LINE_STYLE style,
                             const int curve_segments,
                             const bool draw_back,
                             FP_RenderReport &report)
{
   int i0 = FP_NormalizeIndex(start.index_anchor, rates_total);
   int ic = FP_NormalizeIndex(control.index_anchor, rates_total);
   int i1 = FP_NormalizeIndex(finish.index_anchor, rates_total);
   if(i0 < 0 || ic < 0 || i1 < 0 || i1 <= i0)
   {
      report.fallback_curves++;
      return FP_CreateTrend(base + "fallback", start.time_anchor, start.price, finish.time_anchor, finish.price, c, width, style, draw_back, report);
   }

   int span = i1 - i0;
   int max_segments = MathMax(6, curve_segments);
   int segs = MathMin(MathMax(2, span), max_segments);

   datetime prev_t = FP_TimeAtIndex(rates, rates_total, i0, start.time_anchor);
   double prev_p = start.price;
   int prev_idx = i0;
   int drawn = 0;

   for(int s=1; s<=segs; s++)
   {
      double raw_u = (double)s / (double)segs;
      int idx = i0 + (int)MathRound((double)span * raw_u);
      if(idx <= prev_idx) idx = prev_idx + 1;
      if(idx > i1) idx = i1;
      if(idx <= prev_idx) continue;

      double u = (double)(idx - i0) / (double)span;
      double v = 1.0 - u;
      double p = v*v*start.price + 2.0*v*u*control.price + u*u*finish.price;
      datetime t = FP_TimeAtIndex(rates, rates_total, idx, finish.time_anchor);
      if(t <= prev_t && idx < i1)
      {
         prev_idx = idx;
         continue;
      }

      drawn++;
      FP_CreateTrend(base + IntegerToString(drawn), prev_t, prev_p, t, p, c, width, style, draw_back, report);
      prev_t = t;
      prev_p = p;
      prev_idx = idx;
      if(idx >= i1) break;
   }

   if(drawn == 0)
   {
      report.fallback_curves++;
      return FP_CreateTrend(base + "fallback", start.time_anchor, start.price, finish.time_anchor, finish.price, c, width, style, draw_back, report);
   }
   return true;
}

bool FP_DrawStackedTextR(const string name,
                         const int index_anchor,
                         const datetime time_anchor,
                         const double price,
                         const bool is_peak,
                         const string text,
                         const color c,
                         const int font_size,
                         FP_LabelStackCluster &clusters[],
                         FP_RenderReport &report)
{
   datetime column_time = time_anchor;
   double column_price = price;
   int lane = FP_RegisterLabelCluster(clusters, index_anchor, time_anchor, price, is_peak, column_time, column_price);
   double label_price = column_price + FP_LabelOffsetPrice(lane, is_peak);
   return FP_CreateText(name, column_time, label_price, text, c, font_size, report);
}

void FP_DrawFlagBodyR(const FP_FlagEvent &e,
                      const FP_RenderConfig &cfg,
                      const color c,
                      const int width,
                      const MqlRates &rates[],
                      const int rates_total,
                      FP_RenderReport &report)
{
   if(!e.has_origin || !e.has_leg1) return;
   string base = FP_RenderEventObjectStem(e, cfg);

   if(FP_CreateTrend(base + "leg1", e.origin.time_anchor, e.origin.price, e.leg1.time_anchor, e.leg1.price, c, width, STYLE_SOLID, false, report))
      report.event_body_drawn++;

   if(e.has_waist && e.has_leg2)
   {
      FP_DrawIndexSampledArcR(base + "curve_", e.leg1, e.waist, e.leg2, rates, rates_total, c, width, STYLE_SOLID, cfg.curve_segments, false, report);
   }
}

void FP_DrawProbableLegR(const FP_FlagEvent &e, const FP_RenderConfig &cfg, const color c, const int width, FP_RenderReport &report)
{
   if(!e.has_origin || !e.has_leg1) return;
   string base = FP_RenderEventObjectStem(e, cfg) + "prob";
   if(FP_CreateTrend(base, e.origin.time_anchor, e.origin.price, e.leg1.time_anchor, e.leg1.price, c, width, STYLE_DASH, false, report))
      report.event_probable_drawn++;
}

void FP_DrawInternalLabelsR(const FP_FlagEvent &e,
                            const FP_RenderConfig &cfg,
                            const color c,
                            const int font_size,
                            FP_LabelStackCluster &label_clusters[],
                            FP_RenderReport &report)
{
   string base = FP_RenderEventObjectStem(e, cfg) + "I_";

   FP_Node nums[4];
   nums[0] = e.internal_pack.n1;
   nums[1] = e.internal_pack.n2;
   nums[2] = e.internal_pack.n3;
   nums[3] = e.internal_pack.n4;
   for(int i=0; i<4; i++)
   {
      if(nums[i].id < 0) continue;
      bool is_peak = (nums[i].kind == FP_NODE_HIGH);
      if(FP_DrawStackedTextR(base + IntegerToString(i+1), nums[i].index_anchor, nums[i].time_anchor, nums[i].price, is_peak, IntegerToString(i+1), c, font_size, label_clusters, report))
         report.event_internal_labels++;
   }
}

void FP_DrawOriginLabelR(const FP_FlagEvent &e,
                         const FP_RenderConfig &cfg,
                         const color c,
                         const int font_size,
                         FP_LabelStackCluster &label_clusters[],
                         FP_RenderReport &report)
{
   if(!e.has_origin) return;
   bool is_peak = (e.origin.kind == FP_NODE_HIGH);
   if(FP_DrawStackedTextR(FP_RenderEventObjectStem(e, cfg) + "O", e.origin.index_anchor, e.origin.time_anchor, e.origin.price, is_peak, "O", c, font_size, label_clusters, report))
      report.event_origin_labels++;
}

void FP_DrawHookBranchR(const FP_HookBranch &h,
                        const FP_RenderConfig &cfg,
                        const color c,
                        const int width,
                        const int font_size,
                        FP_LabelStackCluster &label_clusters[],
                        const MqlRates &rates[],
                        const int rates_total,
                        FP_RenderReport &report)
{
   string base = FP_RenderHookObjectStem(h, cfg);

   FP_Node arc_start;
   if(h.has_cycle_start) arc_start = h.cycle_start_node;
   else arc_start = h.start_node;

   FP_DrawIndexSampledArcR(base + "arc_", arc_start, h.extreme_node, h.resolve_node, rates, rates_total, c, width, STYLE_DOT, cfg.curve_segments, cfg.draw_hook_back, report);
   report.hook_arcs_drawn++;

   bool is_peak = (h.resolve_node.kind == FP_NODE_HIGH);
   string label = "ND L" + IntegerToString(h.scale_L) + " #" + IntegerToString(h.node_count);
   if(h.seeds_visible_f1) label = label + " seed";
   if(FP_DrawStackedTextR(base + "label", h.resolve_node.index_anchor, h.resolve_node.time_anchor, h.resolve_node.price, is_peak, label, c, font_size, label_clusters, report))
      report.hook_labels_drawn++;

   if(cfg.show_hook_count_labels)
   {
      FP_Node nums[4];
      nums[0] = h.n1;
      nums[1] = h.n2;
      nums[2] = h.n3;
      nums[3] = h.n4;
      for(int i=0; i<4; i++)
      {
         if(nums[i].id < 0) continue;
         bool np = (nums[i].kind == FP_NODE_HIGH);
         if(FP_DrawStackedTextR(base + "N" + IntegerToString(i+1), nums[i].index_anchor, nums[i].time_anchor, nums[i].price, np, IntegerToString(i+1), c, MathMax(6, font_size-1), label_clusters, report))
            report.hook_count_labels++;
      }
   }
}

bool FP_HookSeedsVisibleF1(const FP_HookBranch &h, const FP_FlagEvent &events[])
{
   double eps = FP_EpsilonPrice(0.0);
   if(h.seeds_visible_f1) return true;
   FP_Node origin = FP_HookOriginNode(h, eps);
   if(origin.id < 0) return false;

   for(int i=0; i<ArraySize(events); i++)
   {
      if(!events[i].visible_main) continue;
      if(events[i].level != FP_LEVEL_F1) continue;
      if(events[i].direction != h.direction) continue;
      if(events[i].scale_L != h.scale_L) continue;
      if(!events[i].has_origin) continue;
      if(events[i].origin.kind != origin.kind) continue;
      if(events[i].origin.index_anchor != origin.index_anchor) continue;
      if(!FP_AlmostEqual(events[i].origin.price, origin.price, eps)) continue;
      return true;
   }
   return false;
}

int FP_DrawAllWithReport(const FP_FlagEvent &events[],
                         const FP_HookBranch &hooks[],
                         const MqlRates &rates[],
                         const int rates_total,
                         const FP_RenderConfig &cfg,
                         FP_RenderReport &report)
{
   FP_ResetRenderReport(report);
   report.attempted = true;
   report.status = "running";
   report.prefix = cfg.prefix;
   report.input_events = ArraySize(events);
   report.input_hooks = ArraySize(hooks);

   for(int ve=0; ve<ArraySize(events); ve++) if(events[ve].visible_main) report.visible_events_seen++;
   for(int vh=0; vh<ArraySize(hooks); vh++) if(hooks[vh].visible_main) report.visible_hooks_seen++;

   if(cfg.delete_existing_by_prefix)
      report.objects_deleted_by_prefix = FP_DeleteObjectsByPrefix(cfg.prefix);

   FP_LabelStackCluster label_clusters[];
   ArrayResize(label_clusters, 0);

   if(cfg.draw_hooks)
   {
      for(int h=0; h<ArraySize(hooks); h++)
      {
         if(cfg.max_hooks_to_draw > 0 && report.drawn_hooks >= cfg.max_hooks_to_draw)
         {
            report.hook_filter_limit++;
            continue;
         }
         bool seeds = FP_HookSeedsVisibleF1(hooks[h], events);
         if(!FP_ShouldRenderHook(hooks[h], seeds, cfg, report)) continue;
         FP_DrawHookBranchR(hooks[h], cfg, cfg.hook_color, MathMax(1, cfg.fixed_line_width), MathMax(6, cfg.label_font_size), label_clusters, rates, rates_total, report);
         if(report.first_drawn_hook_id < 0) report.first_drawn_hook_id = hooks[h].branch_id;
         report.last_drawn_hook_id = hooks[h].branch_id;
         report.drawn_hooks++;
         FP_RenderAddSample(report, "H" + IntegerToString(hooks[h].branch_id) + ":" + FP_RenderSafeId(hooks[h].visual_id, 18), cfg.sample_limit);
      }
   }

   for(int i=0; i<ArraySize(events); i++)
   {
      if(cfg.max_events_to_draw > 0 && report.drawn_events >= cfg.max_events_to_draw)
      {
         report.event_filter_limit++;
         continue;
      }
      FP_FlagEvent e = events[i];
      if(!FP_ShouldRenderEvent(e, cfg, report)) continue;

      color c = FP_ShadeColor(FP_StatusColor(e, cfg.bull_candidate, cfg.bull_confirmed, cfg.bear_candidate, cfg.bear_confirmed, cfg.f3_locked), e.event_id, cfg.use_sequence_color_shades);
      int width = MathMax(1, cfg.fixed_line_width);
      if(e.render_kind == FP_RENDER_FLAG_BODY) FP_DrawFlagBodyR(e, cfg, c, width, rates, rates_total, report);
      else if(e.render_kind == FP_RENDER_PROBABLE) FP_DrawProbableLegR(e, cfg, c, width, report);

      FP_Node anchor;
      if(e.has_leg2) anchor = e.leg2;
      else if(e.has_leg1) anchor = e.leg1;
      else anchor = e.origin;
      if(anchor.id >= 0)
      {
         bool is_peak = (anchor.kind == FP_NODE_HIGH);
         if(FP_DrawStackedTextR(FP_RenderEventObjectStem(e, cfg) + "LBL", anchor.index_anchor, anchor.time_anchor, anchor.price, is_peak, FP_EventLabel(e, cfg.detailed_labels, cfg.show_parent_ids), c, cfg.label_font_size, label_clusters, report))
            report.event_label_drawn++;
      }
      if(cfg.show_origin_labels) FP_DrawOriginLabelR(e, cfg, c, cfg.label_font_size, label_clusters, report);
      if(cfg.show_internal_labels) FP_DrawInternalLabelsR(e, cfg, c, MathMax(6, cfg.label_font_size - 1), label_clusters, report);

      if(report.first_drawn_event_id < 0) report.first_drawn_event_id = e.event_id;
      report.last_drawn_event_id = e.event_id;
      report.drawn_events++;
      FP_RenderAddSample(report, "E" + IntegerToString(e.event_id) + ":" + FP_LevelName(e.level) + ":" + FP_StatusName(e.status) + ":" + FP_RenderSafeId(e.canonical_id, 18), cfg.sample_limit);
   }

   report.drawn_total = report.drawn_events + report.drawn_hooks;
   report.status = (report.ok ? "ok" : "partial");
   if(StringLen(report.reason) <= 0) report.reason = "renderer_readonly_done";
   ChartRedraw(0);
   return report.drawn_total;
}

int FP_DrawAll(const FP_FlagEvent &events[],
               const FP_HookBranch &hooks[],
               const MqlRates &rates[],
               const int rates_total,
               const string prefix,
               const int max_events_to_draw,
               const int max_hooks_to_draw,
               const bool draw_f1,
               const bool draw_f2,
               const bool draw_f3,
               const bool draw_bull,
               const bool draw_bear,
               const bool draw_candidates,
               const bool draw_confirmed,
               const bool draw_locked,
               const bool draw_invalidated,
               const bool draw_hooks,
               const bool draw_only_flag_seed_hooks,
               const bool show_hook_count_labels,
               const bool detailed_labels,
               const bool show_parent_ids,
               const bool show_origin_labels,
               const bool show_internal_labels,
               const bool use_sequence_color_shades,
               const int fixed_line_width,
               const int curve_segments,
               const int label_font_size,
               const color bull_candidate,
               const color bull_confirmed,
               const color bear_candidate,
               const color bear_confirmed,
               const color f3_locked,
               const color hook_color)
{
   FP_RenderConfig cfg;
   FP_DefaultRenderConfig(cfg);
   cfg.prefix = prefix;
   cfg.max_events_to_draw = max_events_to_draw;
   cfg.max_hooks_to_draw = max_hooks_to_draw;
   cfg.draw_f1 = draw_f1;
   cfg.draw_f2 = draw_f2;
   cfg.draw_f3 = draw_f3;
   cfg.draw_bull = draw_bull;
   cfg.draw_bear = draw_bear;
   cfg.draw_candidates = draw_candidates;
   cfg.draw_confirmed = draw_confirmed;
   cfg.draw_locked = draw_locked;
   cfg.draw_invalidated = draw_invalidated;
   cfg.draw_hooks = draw_hooks;
   cfg.draw_only_flag_seed_hooks = draw_only_flag_seed_hooks;
   cfg.show_hook_count_labels = show_hook_count_labels;
   cfg.detailed_labels = detailed_labels;
   cfg.show_parent_ids = show_parent_ids;
   cfg.show_origin_labels = show_origin_labels;
   cfg.show_internal_labels = show_internal_labels;
   cfg.use_sequence_color_shades = use_sequence_color_shades;
   cfg.fixed_line_width = fixed_line_width;
   cfg.curve_segments = curve_segments;
   cfg.label_font_size = label_font_size;
   cfg.bull_candidate = bull_candidate;
   cfg.bull_confirmed = bull_confirmed;
   cfg.bear_candidate = bear_candidate;
   cfg.bear_confirmed = bear_confirmed;
   cfg.f3_locked = f3_locked;
   cfg.hook_color = hook_color;

   FP_RenderReport report;
   return FP_DrawAllWithReport(events, hooks, rates, rates_total, cfg, report);
}

#endif // __FP_RENDERER_MQH__
