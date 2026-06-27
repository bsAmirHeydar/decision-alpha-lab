#ifndef __FCN_RENDERER_MQH__
#define __FCN_RENDERER_MQH__
#property strict
#include "FCN_Types.mqh"

// FlagCountingVNext clean-all renderer
// - Every accepted/provisional event can be visible.
// - All body lines are thin and uniform by default.
// - Sequences inside the same color family receive subtle shade variations.
// - ND / Hook phases are text-only labels so they explain unowned movement without adding line noise.
// - Labels use deterministic peak/valley stacking: above peaks and below valleys.
// - Body curves use dense arc-like Bezier segmentation for a smooth half-circle visual.

void FCN_DeleteObjectsByPrefix(const string prefix)
{
   for(int i=ObjectsTotal(0, -1, -1)-1; i>=0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(StringFind(name, prefix) == 0)
         ObjectDelete(0, name);
   }
}

void FCN_SetCommonObjectProps(const string name)
{
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
}

int FCN_Clamp255(const int v)
{
   if(v < 0) return 0;
   if(v > 255) return 255;
   return v;
}

color FCN_RGB(const int r, const int g, const int b)
{
   int rr = FCN_Clamp255(r);
   int gg = FCN_Clamp255(g);
   int bb = FCN_Clamp255(b);
   return (color)(rr | (gg << 8) | (bb << 16));
}

int FCN_Red(const color c)   { return ((int)c) & 0xFF; }
int FCN_Green(const color c) { return (((int)c) >> 8) & 0xFF; }
int FCN_Blue(const color c)  { return (((int)c) >> 16) & 0xFF; }

color FCN_BlendColor(const color a, const color b, const double t)
{
   double x = MathMax(0.0, MathMin(1.0, t));
   int r = (int)MathRound((1.0 - x) * FCN_Red(a)   + x * FCN_Red(b));
   int g = (int)MathRound((1.0 - x) * FCN_Green(a) + x * FCN_Green(b));
   int bl = (int)MathRound((1.0 - x) * FCN_Blue(a) + x * FCN_Blue(b));
   return FCN_RGB(r, g, bl);
}

color FCN_SequenceShade(const color base, const int sequence_id)
{
   // Same color family, slightly different brightness/saturation per sequence.
   int bucket = MathAbs(sequence_id) % 9; // 0..8
   if(bucket == 4)
      return base;
   if(bucket < 4)
   {
      double t = 0.08 + 0.055 * (double)(4 - bucket);
      return FCN_BlendColor(base, clrBlack, t);
   }
   double t = 0.07 + 0.045 * (double)(bucket - 4);
   return FCN_BlendColor(base, clrWhite, t);
}

bool FCN_DrawTrendRaw(const string name,
                      const datetime t1,
                      const double p1,
                      const datetime t2,
                      const double p2,
                      const color clr,
                      const int width,
                      const ENUM_LINE_STYLE style)
{
   if(t1 <= 0 || t2 <= 0)
      return false;

   ObjectDelete(0, name);
   ResetLastError();
   if(!ObjectCreate(0, name, OBJ_TREND, 0, t1, p1, t2, p2))
   {
      Print("FCN renderer trend create failed name=", name, " err=", GetLastError());
      return false;
   }

   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, false);
   ObjectSetInteger(0, name, OBJPROP_RAY_LEFT, false);
   FCN_SetCommonObjectProps(name);
   return true;
}

bool FCN_DrawTextRaw(const string name,
                     const datetime t,
                     const double price,
                     const string value,
                     const color clr,
                     const int font_size,
                     const ENUM_ANCHOR_POINT anchor = ANCHOR_CENTER)
{
   if(t <= 0 || value == "")
      return false;

   ObjectDelete(0, name);
   ResetLastError();
   if(!ObjectCreate(0, name, OBJ_TEXT, 0, t, price))
   {
      Print("FCN renderer text create failed name=", name, " value=", value, " err=", GetLastError());
      return false;
   }

   ObjectSetString(0, name, OBJPROP_TEXT, value);
   ObjectSetString(0, name, OBJPROP_FONT, "Arial Bold");
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetInteger(0, name, OBJPROP_ANCHOR, anchor);
   FCN_SetCommonObjectProps(name);
   return true;
}

double FCN_Bezier(const double p0, const double p1, const double p2, const double p3, const double u)
{
   double v = 1.0 - u;
   return v*v*v*p0 + 3.0*v*v*u*p1 + 3.0*v*u*u*p2 + u*u*u*p3;
}

void FCN_DrawBezierCurve(const string prefix,
                         const datetime t0,
                         const double p0,
                         const datetime c1t,
                         const double c1p,
                         const datetime c2t,
                         const double c2p,
                         const datetime t3,
                         const double p3,
                         const color clr,
                         const int width,
                         const int segments)
{
   int n = MathMax(18, segments);
   datetime prev_t = t0;
   double prev_p = p0;

   for(int i=1; i<=n; i++)
   {
      double u = (double)i / (double)n;
      datetime next_t = (datetime)MathRound(FCN_Bezier((double)((long)t0),
                                                       (double)((long)c1t),
                                                       (double)((long)c2t),
                                                       (double)((long)t3),
                                                       u));
      double next_p = FCN_Bezier(p0, c1p, c2p, p3, u);
      FCN_DrawTrendRaw(prefix + IntegerToString(i), prev_t, prev_p, next_t, next_p, clr, width, STYLE_SOLID);
      prev_t = next_t;
      prev_p = next_p;
   }
}

int FCN_StatusPriority(const int status)
{
   if(status == FCN_STATUS_TERMINAL)  return 3;
   if(status == FCN_STATUS_CONFIRMED) return 2;
   if(status == FCN_STATUS_LIVE)      return 1;
   return 0;
}

bool FCN_IsHigherDisplayPriority(const FCN_Event &a, const FCN_Event &b)
{
   if(a.scale_L != b.scale_L)
      return a.scale_L > b.scale_L;
   if(a.level != b.level)
      return a.level > b.level;

   int sa = FCN_StatusPriority(a.status);
   int sb = FCN_StatusPriority(b.status);
   if(sa != sb)
      return sa > sb;

   if(a.size != b.size)
      return a.size > b.size;

   return a.event_id < b.event_id;
}

double FCN_EventBodyHeight(const FCN_Event &e)
{
   double h1 = MathAbs(e.leg1.price - e.waist.price);
   double h2 = MathAbs(e.leg2.price - e.waist.price);
   double h3 = MathAbs(e.leg2.price - e.origin.price);
   double h = MathMax(MathMax(h1, h2), h3);
   if(h <= 0.0)
      h = 80.0 * _Point;
   return h;
}

double FCN_ChartPriceRange()
{
   double pmax = 0.0;
   double pmin = 0.0;
   if(ChartGetDouble(0, CHART_PRICE_MAX, 0, pmax) && ChartGetDouble(0, CHART_PRICE_MIN, 0, pmin))
   {
      double r = MathAbs(pmax - pmin);
      if(r > 0.0)
         return r;
   }
   return 1000.0 * _Point;
}

bool FCN_LabelAboveStructure(const FCN_Event &e)
{
   if(e.leg2.kind == FCN_NODE_HIGH)
      return true;
   if(e.leg2.kind == FCN_NODE_LOW)
      return false;
   return e.direction == FCN_DIR_BULLISH;
}

bool FCN_LabelAnchorsOverlap(const FCN_Event &a, const FCN_Event &b)
{
   // Labels are stacked by visual side, not by direction.
   // Peak-side labels go above peaks; valley-side labels go below valleys.
   if(FCN_LabelAboveStructure(a) != FCN_LabelAboveStructure(b))
      return false;

   int sec = PeriodSeconds(_Period);
   if(sec <= 0) sec = 60;

   long dt = (long)MathAbs((double)((long)a.leg2.time - (long)b.leg2.time));
   long max_dt = (long)(sec * MathMax(MathMax(a.scale_L, b.scale_L), 8) * 4);
   if(dt > max_dt)
      return false;

   double chart_range = FCN_ChartPriceRange();
   double tol = MathMax(chart_range * 0.035, 80.0 * _Point);
   return MathAbs(a.leg2.price - b.leg2.price) <= tol;
}

bool FCN_SameEventIdentity(const FCN_Event &a, const FCN_Event &b)
{
   return a.event_id == b.event_id
       && a.sequence_id == b.sequence_id
       && a.scale_L == b.scale_L
       && a.level == b.level
       && a.leg2.time == b.leg2.time;
}


string FCN_EventDisplayLabel(const FCN_Event &e, const bool detailed)
{
   string base = FCN_LevelToString(e.level);
   if(!detailed)
      return base;

   // Compact but traceable identity: level / scale / sequence.
   // This answers "which flag is this?" without changing the detection result.
   return base + "/L" + IntegerToString(e.scale_L) + "/Q" + IntegerToString(e.sequence_id);
}

color FCN_EventColor(const FCN_Event &e,
                     const color bull_live,
                     const color bull_confirmed,
                     const color bear_live,
                     const color bear_confirmed,
                     const color bull_f3_terminal,
                     const color bear_f3_terminal,
                     const color nd_color,
                     const bool use_sequence_shades)
{
   if(e.level == FCN_LEVEL_ND)
      return use_sequence_shades ? FCN_SequenceShade(nd_color, e.sequence_id) : nd_color;

   color base = clrSilver;
   if(e.level == FCN_LEVEL_F3 && e.status == FCN_STATUS_TERMINAL)
      base = (e.direction == FCN_DIR_BULLISH ? bull_f3_terminal : bear_f3_terminal);
   else
   {
      bool confirmed = (e.status == FCN_STATUS_CONFIRMED || e.status == FCN_STATUS_TERMINAL);
      if(e.direction == FCN_DIR_BULLISH)
         base = confirmed ? bull_confirmed : bull_live;
      else if(e.direction == FCN_DIR_BEARISH)
         base = confirmed ? bear_confirmed : bear_live;
   }

   return use_sequence_shades ? FCN_SequenceShade(base, e.sequence_id) : base;
}

void FCN_DrawFBody(const FCN_Event &e,
                   const string p,
                   const color clr,
                   const int width)
{
   bool bullish = (e.direction == FCN_DIR_BULLISH);
   int sec = PeriodSeconds(_Period);
   if(sec <= 0) sec = 60;

   FCN_DrawTrendRaw(p + "L0", e.origin.time, e.origin.price, e.leg1.time, e.leg1.price, clr, width, STYLE_SOLID);

   int dt1 = (int)(e.waist.time - e.leg1.time);
   if(dt1 <= 0) dt1 = sec * 4;
   double h1 = MathAbs(e.leg1.price - e.waist.price);
   if(h1 <= 0.0) h1 = 50.0 * _Point;
   datetime c1t = e.leg1.time + (datetime)MathMax(1, (int)(dt1 * 0.35));
   datetime c2t = e.waist.time - (datetime)MathMax(1, (int)(dt1 * 0.16));
   double c1p = bullish ? e.leg1.price - 0.36 * h1 : e.leg1.price + 0.36 * h1;
   double c2p = bullish ? e.waist.price + 0.08 * h1 : e.waist.price - 0.08 * h1;
   FCN_DrawBezierCurve(p + "A", e.leg1.time, e.leg1.price, c1t, c1p, c2t, c2p, e.waist.time, e.waist.price, clr, width, 28);

   int dt2 = (int)(e.leg2.time - e.waist.time);
   if(dt2 <= 0) dt2 = sec * 4;
   double h2 = MathAbs(e.leg2.price - e.waist.price);
   if(h2 <= 0.0) h2 = 50.0 * _Point;
   datetime c3t = e.waist.time + (datetime)MathMax(1, (int)(dt2 * 0.22));
   datetime c4t = e.leg2.time - (datetime)MathMax(1, (int)(dt2 * 0.18));
   double c3p = bullish ? e.waist.price + 0.08 * h2 : e.waist.price - 0.08 * h2;
   double c4p = bullish ? e.leg2.price - 0.16 * h2 : e.leg2.price + 0.16 * h2;
   FCN_DrawBezierCurve(p + "B", e.waist.time, e.waist.price, c3t, c3p, c4t, c4p, e.leg2.time, e.leg2.price, clr, width, 28);
}

bool FCN_EventPassesDrawFilters(const FCN_Event &e,
                                const bool draw_f1,
                                const bool draw_f2,
                                const bool draw_f3,
                                const bool draw_nd,
                                const bool draw_bullish,
                                const bool draw_bearish,
                                const bool draw_only_confirmed)
{
   if(e.level == FCN_LEVEL_ND && !draw_nd) return false;
   if(e.level == FCN_LEVEL_F1 && !draw_f1) return false;
   if(e.level == FCN_LEVEL_F2 && !draw_f2) return false;
   if(e.level == FCN_LEVEL_F3 && !draw_f3) return false;
   if(e.direction == FCN_DIR_BULLISH && !draw_bullish) return false;
   if(e.direction == FCN_DIR_BEARISH && !draw_bearish) return false;
   if(draw_only_confirmed && e.level != FCN_LEVEL_ND && e.status != FCN_STATUS_CONFIRMED && e.status != FCN_STATUS_TERMINAL) return false;
   return true;
}

int FCN_LevelLabelStackSlot(const FCN_Event &events[],
                            const int total,
                            const FCN_Event &e,
                            const bool draw_f1,
                            const bool draw_f2,
                            const bool draw_f3,
                            const bool draw_nd,
                            const bool draw_bullish,
                            const bool draw_bearish,
                            const bool draw_only_confirmed)
{
   int slot = 0;
   for(int j=0; j<total; j++)
   {
      FCN_Event o = events[j];
      if(o.status == FCN_STATUS_INVALID)
         continue;
      if(!FCN_EventPassesDrawFilters(o, draw_f1, draw_f2, draw_f3, draw_nd, draw_bullish, draw_bearish, draw_only_confirmed))
         continue;
      if(FCN_SameEventIdentity(o, e))
         continue;
      if(!FCN_LabelAnchorsOverlap(o, e))
         continue;
      if(FCN_IsHigherDisplayPriority(o, e))
         slot++;
   }
   return slot;
}

void FCN_DrawEventLabels(const FCN_Event &e,
                         const string p,
                         const color clr,
                         const int level_font,
                         const int internal_font,
                         const int level_stack_slot,
                         const bool show_level_label,
                         const bool show_internal_labels,
                         const bool show_detailed_level_labels,
                         const bool show_origin_labels)
{
   double chart_range = FCN_ChartPriceRange();
   double base_off = MathMax(chart_range * 0.012, 10.0 * _Point);
   double step_off = MathMax(chart_range * 0.020, 18.0 * _Point);

   // Peak labels are above peaks; valley labels are below valleys.
   // The closest label is the highest-priority one: larger scale, higher F-level, stronger status.
   bool above = FCN_LabelAboveStructure(e);

   if(show_level_label)
   {
      double off = base_off + (double)level_stack_slot * step_off;
      double label_price = above ? e.leg2.price + off : e.leg2.price - off;
      ENUM_ANCHOR_POINT anchor = above ? ANCHOR_LEFT_LOWER : ANCHOR_LEFT_UPPER;
      FCN_DrawTextRaw(p + "F", e.leg2.time, label_price, FCN_EventDisplayLabel(e, show_detailed_level_labels), clr, level_font, anchor);
   }

   if(e.level != FCN_LEVEL_ND && show_origin_labels)
   {
      bool origin_above = (e.origin.kind == FCN_NODE_HIGH);
      double ooff = MathMax(chart_range * 0.008, 7.0 * _Point);
      double origin_price = origin_above ? e.origin.price + ooff : e.origin.price - ooff;
      FCN_DrawTextRaw(p + "O", e.origin.time, origin_price, "O", clr, internal_font, origin_above ? ANCHOR_LOWER : ANCHOR_UPPER);
   }

   if(e.level == FCN_LEVEL_ND)
      return;

   double internal_base = MathMax(chart_range * 0.010, 8.0 * _Point);
   double internal_step = MathMax(chart_range * 0.013, 10.0 * _Point);

   if(show_internal_labels && e.has_internal1)
   {
      bool i1_above = (e.internal1.kind == FCN_NODE_HIGH);
      double price1 = i1_above ? e.internal1.price + internal_base : e.internal1.price - internal_base;
      FCN_DrawTextRaw(p + "I1", e.internal1.time, price1, "1", clr, internal_font, i1_above ? ANCHOR_LOWER : ANCHOR_UPPER);
   }

   if(show_internal_labels && e.has_internal2)
   {
      bool i2_above = (e.internal2.kind == FCN_NODE_HIGH);
      double price2 = i2_above ? e.internal2.price + internal_base + internal_step : e.internal2.price - internal_base - internal_step;
      FCN_DrawTextRaw(p + "I2", e.internal2.time, price2, "2", clr, internal_font, i2_above ? ANCHOR_LOWER : ANCHOR_UPPER);
   }
}

int FCN_DrawEvents(const FCN_Event &events[],
                   const int max_events_to_draw,
                   const string prefix,
                   const bool draw_f1,
                   const bool draw_f2,
                   const bool draw_f3,
                   const bool draw_nd,
                   const bool draw_bullish,
                   const bool draw_bearish,
                   const bool draw_only_confirmed,
                   const bool show_level_label,
                   const bool show_internal_labels,
                   const int base_level_font,
                   const int base_internal_font,
                   const color bull_live,
                   const color bull_confirmed,
                   const color bear_live,
                   const color bear_confirmed,
                   const color bull_f3_terminal,
                   const color bear_f3_terminal,
                   const color nd_color,
                   const bool use_sequence_shades,
                   const bool show_detailed_level_labels,
                   const bool show_origin_labels,
                   const int fixed_line_width)
{
   FCN_DeleteObjectsByPrefix(prefix);
   int total = ArraySize(events);
   int drawn = 0;
   int width = MathMax(1, fixed_line_width);

   // Pass 1: body geometry only. ND is text-only and does not add line noise.
   for(int i=total-1; i>=0 && drawn<max_events_to_draw; i--)
   {
      FCN_Event e = events[i];
      if(e.status == FCN_STATUS_INVALID)
         continue;
      if(!FCN_EventPassesDrawFilters(e, draw_f1, draw_f2, draw_f3, draw_nd, draw_bullish, draw_bearish, draw_only_confirmed))
         continue;

      string p = prefix + IntegerToString(drawn) + "_S" + IntegerToString(e.scale_L) + "_Q" + IntegerToString(e.sequence_id) + "_";
      color clr = FCN_EventColor(e, bull_live, bull_confirmed, bear_live, bear_confirmed, bull_f3_terminal, bear_f3_terminal, nd_color, use_sequence_shades);
      if(e.level != FCN_LEVEL_ND)
         FCN_DrawFBody(e, p, clr, width);
      drawn++;
   }

   // Pass 2: labels. All sequences remain visible, but sequence shades help distinguish them.
   int label_count = 0;
   for(int k=total-1; k>=0 && label_count<max_events_to_draw; k--)
   {
      FCN_Event e = events[k];
      if(e.status == FCN_STATUS_INVALID)
         continue;
      if(!FCN_EventPassesDrawFilters(e, draw_f1, draw_f2, draw_f3, draw_nd, draw_bullish, draw_bearish, draw_only_confirmed))
         continue;

      string p = prefix + IntegerToString(label_count) + "_S" + IntegerToString(e.scale_L) + "_Q" + IntegerToString(e.sequence_id) + "_";
      color clr = FCN_EventColor(e, bull_live, bull_confirmed, bear_live, bear_confirmed, bull_f3_terminal, bear_f3_terminal, nd_color, use_sequence_shades);
      int level_font = base_level_font;
      int internal_font = base_internal_font;
      int slot = FCN_LevelLabelStackSlot(events, total, e, draw_f1, draw_f2, draw_f3, draw_nd, draw_bullish, draw_bearish, draw_only_confirmed);
      FCN_DrawEventLabels(e, p, clr, level_font, internal_font, slot, show_level_label, show_internal_labels, show_detailed_level_labels, show_origin_labels);
      label_count++;
   }

   ChartRedraw(0);
   return drawn;
}

#endif
