#ifndef __FC6_RENDERER_MQH__
#define __FC6_RENDERER_MQH__
#property strict
#include "FC6_Types.mqh"

// ============================================================================
// V6 Renderer
// ----------------------------------------------------------------------------
// Rendering is diagnostic. It must never invent structures; it only draws events
// emitted by SequenceEngine. All body lines are thin by default. Sequence
// distinction is by labels and slight shade changes, not by line thickness.
// ============================================================================

void FC6_DeleteObjectsByPrefix(const string prefix)
{
   int total = ObjectsTotal(0, 0, -1);
   for(int i=total-1; i>=0; i--)
   {
      string name = ObjectName(0, i, 0, -1);
      if(StringFind(name, prefix) == 0)
         ObjectDelete(0, name);
   }
}

color FC6_ShadeColor(const color base, const int key, const bool enabled)
{
   if(!enabled) return base;
   // MQL color uses 0x00BBGGRR. Keep changes mild so semantic color family remains.
   int c = (int)base;
   int r = (int)(c & 0xFF);
   int g = (int)((c >> 8) & 0xFF);
   int b = (int)((c >> 16) & 0xFF);
   int delta = ((key % 7) - 3) * 9;
   r = (int)MathMax(0, MathMin(255, r + delta));
   g = (int)MathMax(0, MathMin(255, g + delta));
   b = (int)MathMax(0, MathMin(255, b + delta));
   return (color)(r | (g << 8) | (b << 16));
}

color FC6_EventColor(const FC6_FlagEvent &e,
                     const color bull_candidate,
                     const color bull_confirmed,
                     const color bear_candidate,
                     const color bear_confirmed,
                     const color f3_locked,
                     const bool shade)
{
   color base = clrSilver;
   if(e.level == FC6_LEVEL_F3 && (e.status == FC6_STATUS_COMPLETED || e.status == FC6_STATUS_LOCKED))
      base = f3_locked;
   else if(e.direction == FC6_DIR_BULLISH)
      base = (e.status == FC6_STATUS_CONFIRMED || e.status == FC6_STATUS_COMPLETED || e.status == FC6_STATUS_LOCKED) ? bull_confirmed : bull_candidate;
   else if(e.direction == FC6_DIR_BEARISH)
      base = (e.status == FC6_STATUS_CONFIRMED || e.status == FC6_STATUS_COMPLETED || e.status == FC6_STATUS_LOCKED) ? bear_confirmed : bear_candidate;
   return FC6_ShadeColor(base, e.sequence_id + e.event_id + e.scale_L, shade);
}

int FC6_StatusPriorityForMain(const int status)
{
   if(status == FC6_STATUS_LOCKED) return 70;
   if(status == FC6_STATUS_COMPLETED) return 60;
   if(status == FC6_STATUS_CONFIRMED) return 50;
   if(status == FC6_STATUS_QUALIFIED) return 40;
   if(status == FC6_STATUS_POST_FLAG) return 30;
   if(status == FC6_STATUS_LIVE_BODY) return 20;
   if(status == FC6_STATUS_RAW_SEED) return 10;
   if(status == FC6_STATUS_INVALIDATED) return 0;
   return 0;
}

bool FC6_EventIsLifecycleSuperseded(const FC6_FlagEvent &events[], const int count, const int idx)
{
   if(idx < 0 || idx >= count) return false;
   FC6_FlagEvent e = events[idx];
   for(int j=0; j<count; j++)
   {
      if(j == idx) continue;
      if(events[j].sequence_id != e.sequence_id) continue;
      if(events[j].level != e.level) continue;
      if(events[j].direction != e.direction) continue;
      int pj = FC6_StatusPriorityForMain(events[j].status);
      int pi = FC6_StatusPriorityForMain(e.status);
      if(pj > pi) return true;
      if(pj == pi && events[j].event_id < e.event_id) return true; // older equivalent state is closer to price
   }
   return false;
}

int FC6_EventLabelAnchorIndex(const FC6_FlagEvent &e)
{
   if(e.has_leg2) return e.leg2.index_anchor;
   if(e.has_leg1) return e.leg1.index_anchor;
   if(e.has_origin) return e.origin.index_anchor;
   return -1;
}

double FC6_EventLabelAnchorPrice(const FC6_FlagEvent &e)
{
   if(e.has_leg2) return e.leg2.price;
   if(e.has_leg1) return e.leg1.price;
   if(e.has_origin) return e.origin.price;
   return 0.0;
}

int FC6_ClusterLaneForEvent(const FC6_FlagEvent &events[],
                            const int current_index,
                            const int time_cluster_bars,
                            const double price_cluster_points)
{
   int lane = 0;
   int anchor = FC6_EventLabelAnchorIndex(events[current_index]);
   double price = FC6_EventLabelAnchorPrice(events[current_index]);
   double price_eps = MathMax(1.0, price_cluster_points) * _Point;
   for(int j=0; j<current_index; j++)
   {
      if(events[j].direction != events[current_index].direction) continue;
      int a2 = FC6_EventLabelAnchorIndex(events[j]);
      if(anchor < 0 || a2 < 0) continue;
      if(MathAbs(anchor - a2) > time_cluster_bars) continue;
      if(MathAbs(FC6_EventLabelAnchorPrice(events[j]) - price) > price_eps) continue;
      lane++;
   }
   return MathMin(lane, 32);
}

bool FC6_DrawTrend(const string name,
                   const datetime t1,
                   const double p1,
                   const datetime t2,
                   const double p2,
                   const color clr,
                   const int width,
                   const ENUM_LINE_STYLE style)
{
   ObjectDelete(0, name);
   if(!ObjectCreate(0, name, OBJ_TREND, 0, t1, p1, t2, p2)) return false;
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, false);
   ObjectSetInteger(0, name, OBJPROP_RAY_LEFT, false);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   return true;
}

bool FC6_DrawText(const string name,
                  const datetime t,
                  const double p,
                  const string text,
                  const color clr,
                  const int font_size)
{
   ObjectDelete(0, name);
   if(!ObjectCreate(0, name, OBJ_TEXT, 0, t, p)) return false;
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_CENTER);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
   return true;
}

void FC6_DrawQuadraticCurve(const string prefix,
                            const datetime t0,
                            const double p0,
                            const datetime tc,
                            const double pc,
                            const datetime t1,
                            const double p1,
                            const color clr,
                            const int width,
                            const int segments)
{
   int segs = MathMax(8, segments);
   double x0 = (double)t0;
   double xc = (double)tc;
   double x1 = (double)t1;
   double prevx = x0;
   double prevy = p0;
   for(int i=1; i<=segs; i++)
   {
      double u = (double)i / (double)segs;
      double inv = 1.0 - u;
      double x = inv*inv*x0 + 2.0*inv*u*xc + u*u*x1;
      double y = inv*inv*p0 + 2.0*inv*u*pc + u*u*p1;
      FC6_DrawTrend(prefix + IntegerToString(i), (datetime)prevx, prevy, (datetime)x, y, clr, width, STYLE_SOLID);
      prevx = x;
      prevy = y;
   }
}

void FC6_DrawSmoothFlagBody(const FC6_FlagEvent &e,
                            const string prefix,
                            const color clr,
                            const int width,
                            const int curve_segments)
{
   if(!e.has_origin || !e.has_leg1) return;
   FC6_DrawTrend(prefix + "_L1", e.origin.time_anchor, e.origin.price, e.leg1.time_anchor, e.leg1.price, clr, width, STYLE_SOLID);
   if(!e.has_waist || !e.has_leg2) return;

   // One visual belly from Leg1 to Leg2 through the true correction waist.  MT5
   // has no universal semicircle object, so we approximate with many short
   // segments; with 32+ segments it reads as a clean semi-arc instead of a broken
   // zigzag. The waist is the control point required by the logic engine.
   FC6_DrawQuadraticCurve(prefix + "_ARC_",
                          e.leg1.time_anchor,
                          e.leg1.price,
                          e.waist.time_anchor,
                          e.waist.price,
                          e.leg2.time_anchor,
                          e.leg2.price,
                          clr,
                          width,
                          curve_segments);
}

void FC6_DrawProbableLeg(const FC6_FlagEvent &e,
                         const string prefix,
                         const color clr,
                         const int width)
{
   if(e.has_origin && e.has_leg1)
      FC6_DrawTrend(prefix + "_SEED_L1", e.origin.time_anchor, e.origin.price, e.leg1.time_anchor, e.leg1.price, clr, width, STYLE_DOT);
   if(e.has_leg1 && e.has_waist)
      FC6_DrawTrend(prefix + "_SEED_W", e.leg1.time_anchor, e.leg1.price, e.waist.time_anchor, e.waist.price, clr, width, STYLE_DOT);
}

string FC6_EventLabelText(const FC6_FlagEvent &e, const bool detailed, const bool show_parent)
{
   string base = FC6_LevelToString(e.level);
   if(!detailed) return base;
   string text = base + " L" + IntegerToString(e.scale_L) + " Q" + IntegerToString(e.sequence_id);
   if(show_parent && e.parent_event_id >= 0) text += " P" + IntegerToString(e.parent_event_id);
   text += " " + FC6_StatusToString(e.status);
   return text;
}

double FC6_LabelOffset(const FC6_FlagEvent &e, const int lane, const double point_mult)
{
   double h = 0.0;
   if(e.has_leg1 && e.has_waist) h = MathAbs(e.leg1.price - e.waist.price);
   if(e.has_leg2 && e.has_waist) h = MathMax(h, MathAbs(e.leg2.price - e.waist.price));
   if(h <= 0.0) h = 80.0 * _Point;
   return MathMax(14.0 * _Point, h * point_mult) + (double)lane * MathMax(22.0 * _Point, h * 0.085);
}

void FC6_DrawEventLabels(const FC6_FlagEvent &e,
                         const string prefix,
                         const color clr,
                         const bool show_origin,
                         const bool show_internal,
                         const bool detailed,
                         const bool show_parent,
                         const int font_size,
                         const int lane)
{
   if(e.has_leg2)
   {
      double off = FC6_LabelOffset(e, lane, 0.04);
      double p = e.direction == FC6_DIR_BULLISH ? e.leg2.price + off : e.leg2.price - off;
      FC6_DrawText(prefix + "_LBL", e.leg2.time_anchor, p, FC6_EventLabelText(e, detailed, show_parent), clr, font_size);
   }
   else if(e.has_leg1)
   {
      double off = FC6_LabelOffset(e, lane, 0.04);
      double p = e.direction == FC6_DIR_BULLISH ? e.leg1.price + off : e.leg1.price - off;
      FC6_DrawText(prefix + "_LBL", e.leg1.time_anchor, p, FC6_EventLabelText(e, detailed, show_parent), clr, font_size);
   }

   if(show_origin && e.has_origin)
   {
      double off = 8.0 * _Point;
      double p = e.direction == FC6_DIR_BULLISH ? e.origin.price - off : e.origin.price + off;
      FC6_DrawText(prefix + "_O", e.origin.time_anchor, p, "O", clr, MathMax(6, font_size - 1));
   }

   if(show_internal && e.internal_pack.count > 0)
   {
      for(int k=1; k<=MathMin(e.internal_pack.count, 4); k++)
      {
         FC6_Node n = FC6_ReadInternalNode(e.internal_pack, k);
         if(!FC6_NodeValid(n)) continue;
         double off = (8.0 + 4.0 * k) * _Point;
         double p = e.direction == FC6_DIR_BULLISH ? n.price - off : n.price + off;
         FC6_DrawText(prefix + "_I" + IntegerToString(k), n.time_anchor, p, IntegerToString(k), clr, MathMax(6, font_size - 1));
      }
      if(e.internal_pack.is_nd)
      {
         FC6_Node last = FC6_ReadInternalNode(e.internal_pack, e.internal_pack.count);
         if(FC6_NodeValid(last))
         {
            double off = (18.0 + 5.0 * e.internal_pack.count) * _Point;
            double p = e.direction == FC6_DIR_BULLISH ? last.price - off : last.price + off;
            FC6_DrawText(prefix + "_ND", last.time_anchor, p, "ND", clrGray, MathMax(6, font_size - 1));
         }
      }
   }
}

void FC6_DrawHookArc(const FC6_HookBranch &h,
                     const string prefix,
                     const color clr,
                     const int width,
                     const int segments,
                     const int font_size)
{
   if(!h.is_nd) return;
   if(!FC6_NodeValid(h.start_node) || !FC6_NodeValid(h.extreme_node) || !FC6_NodeValid(h.resolve_node)) return;
   FC6_DrawQuadraticCurve(prefix + "_HOOK_",
                          h.start_node.time_anchor,
                          h.start_node.price,
                          h.extreme_node.time_anchor,
                          h.extreme_node.price,
                          h.resolve_node.time_anchor,
                          h.resolve_node.price,
                          clr,
                          width,
                          segments);
   double off = 12.0 * _Point + (double)(h.branch_id % 8) * 7.0 * _Point;
   double p = h.direction == FC6_DIR_BULLISH ? h.resolve_node.price - off : h.resolve_node.price + off;
   string label = "ND L" + IntegerToString(h.scale_L) + " H" + IntegerToString(h.branch_id);
   FC6_DrawText(prefix + "_HOOK_LBL", h.resolve_node.time_anchor, p, label, clr, font_size);
}



bool FC6_EventHasEarlierVisualEquivalent(const FC6_FlagEvent &events[],
                                         const int count,
                                         const int idx,
                                         const double eps)
{
   if(idx < 0 || idx >= count) return false;
   FC6_FlagEvent e = events[idx];
   if(!e.has_origin || !e.has_leg1) return false;
   for(int j=0; j<idx; j++)
   {
      if(events[j].level != e.level) continue;
      if(events[j].direction != e.direction) continue;
      if(events[j].status != e.status) continue;
      if(!events[j].has_origin || !events[j].has_leg1) continue;
      if(FC6_SameBodyIdentity(events[j], e, eps))
         return true;
   }
   return false;
}

bool FC6_EventIsWeakerVisualDuplicate(const FC6_FlagEvent &events[],
                                      const int count,
                                      const int idx,
                                      const double eps)
{
   if(idx < 0 || idx >= count) return false;
   FC6_FlagEvent e = events[idx];
   if(!e.has_origin || !e.has_leg1) return false;
   int pi = FC6_StatusPriorityForMain(e.status);
   for(int j=0; j<count; j++)
   {
      if(j == idx) continue;
      if(events[j].level != e.level) continue;
      if(events[j].direction != e.direction) continue;
      if(!events[j].has_origin || !events[j].has_leg1) continue;
      if(!FC6_SameBodyIdentity(events[j], e, eps)) continue;
      int pj = FC6_StatusPriorityForMain(events[j].status);
      if(pj > pi) return true;
      if(pj == pi && j < idx) return true;
   }
   return false;
}

bool FC6_EventPassesDrawFilters(const FC6_FlagEvent &e,
                                const bool draw_f1,
                                const bool draw_f2,
                                const bool draw_f3,
                                const bool draw_bull,
                                const bool draw_bear,
                                const bool draw_candidates,
                                const bool draw_confirmed,
                                const bool draw_locked,
                                const bool draw_invalid,
                                const bool draw_raw_seeds)
{
   if(e.level == FC6_LEVEL_F1 && !draw_f1) return false;
   if(e.level == FC6_LEVEL_F2 && !draw_f2) return false;
   if(e.level == FC6_LEVEL_F3 && !draw_f3) return false;
   if(e.direction == FC6_DIR_BULLISH && !draw_bull) return false;
   if(e.direction == FC6_DIR_BEARISH && !draw_bear) return false;
   if(e.status == FC6_STATUS_INVALIDATED && !draw_invalid) return false;
   if(e.status == FC6_STATUS_RAW_SEED && !draw_raw_seeds) return false;
   if(e.status == FC6_STATUS_LOCKED && !draw_locked) return false;
   if((e.status == FC6_STATUS_CONFIRMED || e.status == FC6_STATUS_COMPLETED) && !draw_confirmed) return false;
   if((e.status == FC6_STATUS_RAW_SEED || e.status == FC6_STATUS_LIVE_BODY || e.status == FC6_STATUS_POST_FLAG || e.status == FC6_STATUS_QUALIFIED) && !draw_candidates) return false;
   return true;
}

int FC6_DrawAll(const FC6_FlagEvent &events[],
                const FC6_HookBranch &hooks[],
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
                const bool draw_invalid,
                const bool draw_raw_seeds,
                const bool draw_lifecycle_history,
                const bool skip_visual_duplicates,
                const bool draw_hooks,
                const bool detailed_labels,
                const bool show_parent_ids,
                const bool show_origin,
                const bool show_internal,
                const bool use_shades,
                const int line_width,
                const int curve_segments,
                const int label_font,
                const int label_time_cluster_bars,
                const double label_price_cluster_points,
                const color bull_candidate,
                const color bull_confirmed,
                const color bear_candidate,
                const color bear_confirmed,
                const color f3_locked_color,
                const color hook_color)
{
   FC6_DeleteObjectsByPrefix(prefix);
   int drawn = 0;
   int n = ArraySize(events);
   int start = 0;
   if(max_events_to_draw > 0 && n > max_events_to_draw) start = n - max_events_to_draw;

   for(int i=start; i<n; i++)
   {
      FC6_FlagEvent e = events[i];
      if(!FC6_EventPassesDrawFilters(e, draw_f1, draw_f2, draw_f3, draw_bull, draw_bear, draw_candidates, draw_confirmed, draw_locked, draw_invalid, draw_raw_seeds))
         continue;
      if(!draw_lifecycle_history && FC6_EventIsLifecycleSuperseded(events, n, i))
         continue;
      if(skip_visual_duplicates && FC6_EventIsWeakerVisualDuplicate(events, n, i, _Point * 0.25))
         continue;
      color clr = FC6_EventColor(e, bull_candidate, bull_confirmed, bear_candidate, bear_confirmed, f3_locked_color, use_shades);
      string p = prefix + "E" + IntegerToString(e.event_id) + "_" + FC6_LevelToString(e.level) + "_L" + IntegerToString(e.scale_L);
      if(e.has_leg2)
         FC6_DrawSmoothFlagBody(e, p, clr, MathMax(1, line_width), MathMax(16, curve_segments));
      else
         FC6_DrawProbableLeg(e, p, clr, MathMax(1, line_width));
      int cluster_bars = (label_time_cluster_bars < 0 ? 0 : label_time_cluster_bars);
      int lane = FC6_ClusterLaneForEvent(events, i, cluster_bars, label_price_cluster_points);
      FC6_DrawEventLabels(e, p, clr, show_origin, show_internal, detailed_labels, show_parent_ids, label_font, lane);
      drawn++;
   }

   if(draw_hooks)
   {
      int hn = ArraySize(hooks);
      int hs = 0;
      if(max_hooks_to_draw > 0 && hn > max_hooks_to_draw) hs = hn - max_hooks_to_draw;
      for(int h=hs; h<hn; h++)
      {
         string p = prefix + "H" + IntegerToString(hooks[h].branch_id) + "_L" + IntegerToString(hooks[h].scale_L);
         FC6_DrawHookArc(hooks[h], p, hook_color, MathMax(1, line_width), MathMax(16, curve_segments), MathMax(6, label_font - 1));
      }
   }
   return drawn;
}

#endif // __FC6_RENDERER_MQH__
