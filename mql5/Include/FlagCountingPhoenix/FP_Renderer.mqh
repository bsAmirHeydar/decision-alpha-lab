#ifndef __FP_RENDERER_MQH__
#define __FP_RENDERER_MQH__
#property strict

#include "FP_SequenceEngine.mqh"

// ============================================================================
// Phoenix Renderer
// ----------------------------------------------------------------------------
// Renderer is non-authoritative. It draws only emitted semantic events/hooks.
// It never creates or infers market structure by itself.
// ============================================================================

void FP_DeleteObjectsByPrefix(const string prefix)
{
   int total = ObjectsTotal(0, -1, -1);
   for(int i=total-1; i>=0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(StringFind(name, prefix) == 0) ObjectDelete(0, name);
   }
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

bool FP_DrawTrend(const string name, const datetime t1, const double p1, const datetime t2, const double p2, const color c, const int width, const ENUM_LINE_STYLE style)
{
   if(ObjectFind(0, name) >= 0) ObjectDelete(0, name);
   if(!ObjectCreate(0, name, OBJ_TREND, 0, t1, p1, t2, p2)) return false;
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, false);
   ObjectSetInteger(0, name, OBJPROP_RAY_LEFT, false);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTED, false);
   return true;
}

bool FP_DrawText(const string name, const datetime t, const double p, const string text, const color c, const int font_size)
{
   if(ObjectFind(0, name) >= 0) ObjectDelete(0, name);
   if(!ObjectCreate(0, name, OBJ_TEXT, 0, t, p)) return false;
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
      s = s + " O" + IntegerToString(e.origin.id);
      if(e.has_leg1) s = s + " A" + IntegerToString(e.leg1.id);
      if(e.has_waist) s = s + " W" + IntegerToString(e.waist.id);
      if(e.has_leg2) s = s + " B" + IntegerToString(e.leg2.id);
   }
   return s;
}

double FP_LabelStepPrice()
{
   // Chart-readable vertical step.  A point-only offset is too small on
   // indices, gold, and zoomed M1 charts; text becomes unreadable.  This
   // function combines a symbol-safe point floor with a viewport-relative
   // step so labels form clear vertical columns under/above each other.
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

double FP_LabelOffsetPrice(const int lane, const int direction, const bool is_peak)
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
   // Wider than the old 6-bar cluster so nearby labels use one readable
   // vertical column rather than many overlapping columns.
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

bool FP_DrawStackedText(const string name,
                        const int index_anchor,
                        const datetime time_anchor,
                        const double price,
                        const bool is_peak,
                        const string text,
                        const color c,
                        const int font_size,
                        FP_LabelStackCluster &clusters[])
{
   datetime column_time = time_anchor;
   double column_price = price;
   int lane = FP_RegisterLabelCluster(clusters, index_anchor, time_anchor, price, is_peak, column_time, column_price);
   double label_price = column_price + FP_LabelOffsetPrice(lane, 0, is_peak);
   return FP_DrawText(name, column_time, label_price, text, c, font_size);
}

void FP_DrawFlagBody(const FP_FlagEvent &e,
                     const string prefix,
                     const color c,
                     const int width,
                     const int curve_segments)
{
   if(!e.has_origin || !e.has_leg1) return;
   string base = prefix + "EV_" + IntegerToString(e.event_id) + "_";

   // Origin -> Leg1 straight leg.
   FP_DrawTrend(base + "leg1", e.origin.time_anchor, e.origin.price, e.leg1.time_anchor, e.leg1.price, c, width, STYLE_SOLID);

   if(e.has_waist && e.has_leg2)
   {
      // Smooth quadratic Bezier from Leg1 to Leg2 through Waist as control.
      int segs = MathMax(6, curve_segments);
      datetime t0 = e.leg1.time_anchor;
      datetime tc = e.waist.time_anchor;
      datetime t1 = e.leg2.time_anchor;
      double p0 = e.leg1.price;
      double pc = e.waist.price;
      double p1 = e.leg2.price;
      datetime prev_t = t0;
      double prev_p = p0;
      for(int s=1; s<=segs; s++)
      {
         double u = (double)s / (double)segs;
         double v = 1.0 - u;
         double p = v*v*p0 + 2.0*v*u*pc + u*u*p1;
         long tt = (long)((double)t0 * v*v + 2.0*v*u*(double)tc + u*u*(double)t1);
         datetime t = (datetime)tt;
         FP_DrawTrend(base + "curve_" + IntegerToString(s), prev_t, prev_p, t, p, c, width, STYLE_SOLID);
         prev_t = t;
         prev_p = p;
      }
   }
}

void FP_DrawProbableLeg(const FP_FlagEvent &e, const string prefix, const color c, const int width)
{
   if(!e.has_origin || !e.has_leg1) return;
   string base = prefix + "EV_" + IntegerToString(e.event_id) + "_prob";
   FP_DrawTrend(base, e.origin.time_anchor, e.origin.price, e.leg1.time_anchor, e.leg1.price, c, width, STYLE_DASH);
}

void FP_DrawInternalLabels(const FP_FlagEvent &e, const string prefix, const color c, const int font_size,
                           FP_LabelStackCluster &label_clusters[])
{
   string base = prefix + "EV_" + IntegerToString(e.event_id) + "_I_";

   FP_Node nums[4];
   nums[0] = e.internal_pack.n1;
   nums[1] = e.internal_pack.n2;
   nums[2] = e.internal_pack.n3;
   nums[3] = e.internal_pack.n4;
   for(int i=0; i<4; i++)
   {
      if(nums[i].id < 0) continue;
      bool is_peak = (nums[i].kind == FP_NODE_HIGH);
      FP_DrawStackedText(base + IntegerToString(i+1),
                         nums[i].index_anchor,
                         nums[i].time_anchor,
                         nums[i].price,
                         is_peak,
                         IntegerToString(i+1),
                         c,
                         font_size,
                         label_clusters);
   }
}

void FP_DrawOriginLabel(const FP_FlagEvent &e, const string prefix, const color c, const int font_size,
                        FP_LabelStackCluster &label_clusters[])
{
   if(!e.has_origin) return;
   bool is_peak = (e.origin.kind == FP_NODE_HIGH);
   FP_DrawStackedText(prefix + "EV_" + IntegerToString(e.event_id) + "_O",
                      e.origin.index_anchor,
                      e.origin.time_anchor,
                      e.origin.price,
                      is_peak,
                      "O",
                      c,
                      font_size,
                      label_clusters);
}

void FP_DrawHookBranch(const FP_HookBranch &h, const string prefix, const color c, const int width, const int curve_segments, const int font_size,
                       FP_LabelStackCluster &label_clusters[])
{
   if(!h.is_nd) return;
   string base = prefix + "HK_" + IntegerToString(h.branch_id) + "_";
   datetime t0 = h.start_node.time_anchor;
   datetime tc = h.extreme_node.time_anchor;
   datetime t1 = h.resolve_node.time_anchor;
   double p0 = h.start_node.price;
   double pc = h.extreme_node.price;
   double p1 = h.resolve_node.price;
   int segs = MathMax(6, curve_segments);
   datetime prev_t = t0;
   double prev_p = p0;
   for(int s=1; s<=segs; s++)
   {
      double u = (double)s / (double)segs;
      double v = 1.0 - u;
      double p = v*v*p0 + 2.0*v*u*pc + u*u*p1;
      long tt = (long)((double)t0 * v*v + 2.0*v*u*(double)tc + u*u*(double)t1);
      datetime t = (datetime)tt;
      FP_DrawTrend(base + "arc_" + IntegerToString(s), prev_t, prev_p, t, p, c, width, STYLE_DOT);
      prev_t = t;
      prev_p = p;
   }
   bool is_peak = (h.resolve_node.kind == FP_NODE_HIGH);
   string label = "ND L" + IntegerToString(h.scale_L) + " #" + IntegerToString(h.node_count);
   FP_DrawStackedText(base + "label",
                      h.resolve_node.index_anchor,
                      h.resolve_node.time_anchor,
                      h.resolve_node.price,
                      is_peak,
                      label,
                      c,
                      font_size,
                      label_clusters);

   // Show counted branch numbers on same-side nodes so the hook sequence can be
   // audited visually.
   FP_Node nums[4];
   nums[0] = h.n1;
   nums[1] = h.n2;
   nums[2] = h.n3;
   nums[3] = h.n4;
   for(int i=0; i<4; i++)
   {
      if(nums[i].id < 0) continue;
      bool np = (nums[i].kind == FP_NODE_HIGH);
      FP_DrawStackedText(base + "N" + IntegerToString(i+1),
                         nums[i].index_anchor,
                         nums[i].time_anchor,
                         nums[i].price,
                         np,
                         IntegerToString(i+1),
                         c,
                         MathMax(6, font_size-1),
                         label_clusters);
   }
}

bool FP_ShouldDrawEvent(const FP_FlagEvent &e,
                        const bool draw_f1,
                        const bool draw_f2,
                        const bool draw_f3,
                        const bool draw_bull,
                        const bool draw_bear,
                        const bool draw_candidates,
                        const bool draw_confirmed,
                        const bool draw_locked,
                        const bool draw_invalidated)
{
   if(!e.visible_main) return false;
   if(e.level == FP_LEVEL_F1 && !draw_f1) return false;
   if(e.level == FP_LEVEL_F2 && !draw_f2) return false;
   if(e.level == FP_LEVEL_F3 && !draw_f3) return false;
   if(e.direction == FP_DIR_BULLISH && !draw_bull) return false;
   if(e.direction == FP_DIR_BEARISH && !draw_bear) return false;
   if(e.status == FP_STATUS_INVALIDATED && !draw_invalidated) return false;
   if((e.status == FP_STATUS_SEED || e.status == FP_STATUS_LIVE_LEG || e.status == FP_STATUS_LIVE_BODY || e.status == FP_STATUS_POST_FLAG || e.status == FP_STATUS_QUALIFIED) && !draw_candidates) return false;
   if(e.status == FP_STATUS_CONFIRMED && !draw_confirmed) return false;
   if((e.status == FP_STATUS_COMPLETED || e.status == FP_STATUS_LOCKED) && !draw_locked) return false;
   return true;
}

int FP_DrawAll(const FP_FlagEvent &events[],
               const FP_HookBranch &hooks[],
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
   FP_DeleteObjectsByPrefix(prefix);
   int drawn = 0;
   int hook_drawn = 0;
   FP_LabelStackCluster label_clusters[];
   ArrayResize(label_clusters, 0);

   if(draw_hooks)
   {
      for(int h=0; h<ArraySize(hooks); h++)
      {
         if(max_hooks_to_draw > 0 && hook_drawn >= max_hooks_to_draw) break;
         FP_DrawHookBranch(hooks[h], prefix, hook_color, MathMax(1, fixed_line_width), curve_segments, MathMax(6, label_font_size), label_clusters);
         hook_drawn++;
      }
   }

   for(int i=0; i<ArraySize(events); i++)
   {
      if(max_events_to_draw > 0 && drawn >= max_events_to_draw) break;
      FP_FlagEvent e = events[i];
      if(!FP_ShouldDrawEvent(e, draw_f1, draw_f2, draw_f3, draw_bull, draw_bear, draw_candidates, draw_confirmed, draw_locked, draw_invalidated)) continue;

      color c = FP_ShadeColor(FP_StatusColor(e, bull_candidate, bull_confirmed, bear_candidate, bear_confirmed, f3_locked), e.event_id, use_sequence_color_shades);
      int width = MathMax(1, fixed_line_width);
      if(e.render_kind == FP_RENDER_FLAG_BODY) FP_DrawFlagBody(e, prefix, c, width, curve_segments);
      else if(e.render_kind == FP_RENDER_PROBABLE) FP_DrawProbableLeg(e, prefix, c, width);

      // Main label at Leg2 if body exists, otherwise at Leg1.
      FP_Node anchor = e.has_leg2 ? e.leg2 : e.leg1;
      if(anchor.id >= 0)
      {
         bool is_peak = (anchor.kind == FP_NODE_HIGH);
         FP_DrawStackedText(prefix + "EV_" + IntegerToString(e.event_id) + "_LBL",
                            anchor.index_anchor,
                            anchor.time_anchor,
                            anchor.price,
                            is_peak,
                            FP_EventLabel(e, detailed_labels, show_parent_ids),
                            c,
                            label_font_size,
                            label_clusters);
      }
      if(show_origin_labels) FP_DrawOriginLabel(e, prefix, c, label_font_size, label_clusters);
      if(show_internal_labels) FP_DrawInternalLabels(e, prefix, c, MathMax(6, label_font_size - 1), label_clusters);
      drawn++;
   }
   ChartRedraw(0);
   return drawn + hook_drawn;
}

#endif // __FP_RENDERER_MQH__
