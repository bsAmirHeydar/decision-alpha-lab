#ifndef __FCN_RENDERER_MQH__
#define __FCN_RENDERER_MQH__
#property strict
#include "FCN_Types.mqh"

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

bool FCN_DrawTrendRaw(const string name,
                      const datetime t1,
                      const double p1,
                      const datetime t2,
                      const double p2,
                      const color clr,
                      const int width,
                      const ENUM_LINE_STYLE style)
{
   if(t1 <= 0 || t2 <= 0) return false;
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
   if(t <= 0 || value == "") return false;
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
   int n = MathMax(6, segments);
   datetime prev_t = t0;
   double prev_p = p0;
   for(int i=1; i<=n; i++)
   {
      double u = (double)i / (double)n;
      datetime next_t = (datetime)MathRound(FCN_Bezier((double)((long)t0), (double)((long)c1t), (double)((long)c2t), (double)((long)t3), u));
      double next_p = FCN_Bezier(p0, c1p, c2p, p3, u);
      FCN_DrawTrendRaw(prefix + IntegerToString(i), prev_t, prev_p, next_t, next_p, clr, width, STYLE_SOLID);
      prev_t = next_t;
      prev_p = next_p;
   }
}

int FCN_ScaleRankWidth(const int scale_L)
{
   if(scale_L >= 21) return 4;
   if(scale_L >= 13) return 3;
   if(scale_L >= 8)  return 2;
   return 1;
}

int FCN_ScaleRankFont(const int scale_L, const int base_font)
{
   if(scale_L >= 21) return base_font + 3;
   if(scale_L >= 13) return base_font + 2;
   if(scale_L >= 8)  return base_font + 1;
   return base_font;
}

color FCN_EventColor(const FCN_Event &e,
                     const color bull_live,
                     const color bull_confirmed,
                     const color bear_live,
                     const color bear_confirmed,
                     const color bull_f3_terminal,
                     const color bear_f3_terminal)
{
   if(e.level == FCN_LEVEL_F3 && e.status == FCN_STATUS_TERMINAL)
      return (e.direction == FCN_DIR_BULLISH ? bull_f3_terminal : bear_f3_terminal);

   bool confirmed = (e.status == FCN_STATUS_CONFIRMED || e.status == FCN_STATUS_TERMINAL);
   if(e.direction == FCN_DIR_BULLISH)
      return confirmed ? bull_confirmed : bull_live;
   if(e.direction == FCN_DIR_BEARISH)
      return confirmed ? bear_confirmed : bear_live;
   return clrSilver;
}

void FCN_DrawFBody(const FCN_Event &e,
                   const string p,
                   const color clr,
                   const int width)
{
   bool bullish = (e.direction == FCN_DIR_BULLISH);
   int sec = PeriodSeconds(_Period);
   if(sec <= 0) sec = 60;

   // Leg1 is a straight trend line.
   FCN_DrawTrendRaw(p + "L0", e.origin.time, e.origin.price, e.leg1.time, e.leg1.price, clr, width, STYLE_SOLID);

   // Body curve: one clean belly from Leg1 to Leg2, touching the Waist node.
   int dt1 = (int)(e.waist.time - e.leg1.time);
   if(dt1 <= 0) dt1 = sec * 4;
   double h1 = MathAbs(e.leg1.price - e.waist.price);
   if(h1 <= 0.0) h1 = 50.0 * _Point;
   datetime c1t = e.leg1.time + (datetime)MathMax(1, (int)(dt1 * 0.35));
   datetime c2t = e.waist.time - (datetime)MathMax(1, (int)(dt1 * 0.16));
   double c1p = bullish ? e.leg1.price - 0.36 * h1 : e.leg1.price + 0.36 * h1;
   double c2p = bullish ? e.waist.price + 0.08 * h1 : e.waist.price - 0.08 * h1;
   FCN_DrawBezierCurve(p + "A", e.leg1.time, e.leg1.price, c1t, c1p, c2t, c2p, e.waist.time, e.waist.price, clr, width, 10);

   int dt2 = (int)(e.leg2.time - e.waist.time);
   if(dt2 <= 0) dt2 = sec * 4;
   double h2 = MathAbs(e.leg2.price - e.waist.price);
   if(h2 <= 0.0) h2 = 50.0 * _Point;
   datetime c3t = e.waist.time + (datetime)MathMax(1, (int)(dt2 * 0.22));
   datetime c4t = e.leg2.time - (datetime)MathMax(1, (int)(dt2 * 0.18));
   double c3p = bullish ? e.waist.price + 0.08 * h2 : e.waist.price - 0.08 * h2;
   double c4p = bullish ? e.leg2.price - 0.16 * h2 : e.leg2.price + 0.16 * h2;
   FCN_DrawBezierCurve(p + "B", e.waist.time, e.waist.price, c3t, c3p, c4t, c4p, e.leg2.time, e.leg2.price, clr, width, 10);
}

void FCN_DrawEventLabels(const FCN_Event &e,
                         const string p,
                         const color clr,
                         const int level_font,
                         const int internal_font,
                         const bool show_level_label,
                         const bool show_internal_labels)
{
   bool bullish = e.direction == FCN_DIR_BULLISH;
   double h = MathMax(MathAbs(e.leg1.price - e.waist.price), MathAbs(e.leg2.price - e.waist.price));
   if(h <= 0.0) h = 50.0 * _Point;

   if(show_level_label)
   {
      double off = MathMax(0.06 * h, 8.0 * _Point);
      double label_price = bullish ? e.leg2.price + off : e.leg2.price - off;
      FCN_DrawTextRaw(p + "F", e.leg2.time, label_price, FCN_LevelToString(e.level), clr, level_font,
                      bullish ? ANCHOR_LEFT_LOWER : ANCHOR_LEFT_UPPER);
   }

   if(show_internal_labels && e.has_internal1)
   {
      double off1 = MathMax(0.05 * h, 8.0 * _Point);
      double price1 = bullish ? e.internal1.price - off1 : e.internal1.price + off1;
      FCN_DrawTextRaw(p + "I1", e.internal1.time, price1, "1", clr, internal_font, ANCHOR_CENTER);
   }

   if(show_internal_labels && e.has_internal2)
   {
      double off2 = MathMax(0.05 * h, 8.0 * _Point);
      double price2 = bullish ? e.internal2.price - off2 : e.internal2.price + off2;
      FCN_DrawTextRaw(p + "I2", e.internal2.time, price2, "2", clr, internal_font, ANCHOR_CENTER);
   }
}

bool FCN_EventPassesDrawFilters(const FCN_Event &e,
                                const bool draw_f1,
                                const bool draw_f2,
                                const bool draw_f3,
                                const bool draw_bullish,
                                const bool draw_bearish,
                                const bool draw_only_confirmed)
{
   if(e.level == FCN_LEVEL_F1 && !draw_f1) return false;
   if(e.level == FCN_LEVEL_F2 && !draw_f2) return false;
   if(e.level == FCN_LEVEL_F3 && !draw_f3) return false;
   if(e.direction == FCN_DIR_BULLISH && !draw_bullish) return false;
   if(e.direction == FCN_DIR_BEARISH && !draw_bearish) return false;
   if(draw_only_confirmed && e.status != FCN_STATUS_CONFIRMED && e.status != FCN_STATUS_TERMINAL) return false;
   return true;
}

int FCN_DrawEvents(const FCN_Event &events[],
                   const int max_events_to_draw,
                   const string prefix,
                   const bool draw_f1,
                   const bool draw_f2,
                   const bool draw_f3,
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
                   const color bear_f3_terminal)
{
   FCN_DeleteObjectsByPrefix(prefix);
   int total = ArraySize(events);
   int drawn = 0;

   for(int i=total-1; i>=0 && drawn<max_events_to_draw; i--)
   {
      FCN_Event e = events[i];
      if(e.status == FCN_STATUS_INVALID) continue;
      if(!FCN_EventPassesDrawFilters(e, draw_f1, draw_f2, draw_f3, draw_bullish, draw_bearish, draw_only_confirmed))
         continue;

      string p = prefix + IntegerToString(drawn) + "_S" + IntegerToString(e.scale_L) + "_Q" + IntegerToString(e.sequence_id) + "_";
      color clr = FCN_EventColor(e, bull_live, bull_confirmed, bear_live, bear_confirmed, bull_f3_terminal, bear_f3_terminal);
      int width = FCN_ScaleRankWidth(e.scale_L);
      int level_font = FCN_ScaleRankFont(e.scale_L, base_level_font);
      int internal_font = FCN_ScaleRankFont(e.scale_L, base_internal_font);
      FCN_DrawFBody(e, p, clr, width);
      FCN_DrawEventLabels(e, p, clr, level_font, internal_font, show_level_label, show_internal_labels);
      drawn++;
   }

   ChartRedraw(0);
   return drawn;
}

#endif
