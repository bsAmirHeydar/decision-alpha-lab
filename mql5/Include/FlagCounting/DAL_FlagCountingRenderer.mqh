#ifndef __DAL_FLAG_COUNTING_RENDERER_MQH__
#define __DAL_FLAG_COUNTING_RENDERER_MQH__
#property strict
#include "DAL_FlagCountingTypes.mqh"

void FC_DeleteObjectsByPrefix(const string prefix)
{
   for(int i=ObjectsTotal(0, -1, -1)-1; i>=0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(StringFind(name, prefix) == 0)
         ObjectDelete(0, name);
   }
}

void FC_SetCommonObjectProps(const string name)
{
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
}

bool FC_DrawTrendRaw(const string name,
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
      Print("FC renderer: trend create failed name=", name, " err=", GetLastError());
      return false;
   }
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, false);
   ObjectSetInteger(0, name, OBJPROP_RAY_LEFT, false);
   FC_SetCommonObjectProps(name);
   return true;
}

bool FC_DrawTextRaw(const string name,
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
      Print("FC renderer: text create failed name=", name, " value=", value, " err=", GetLastError());
      return false;
   }
   ObjectSetString(0, name, OBJPROP_TEXT, value);
   ObjectSetString(0, name, OBJPROP_FONT, "Arial Bold");
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetInteger(0, name, OBJPROP_ANCHOR, anchor);
   FC_SetCommonObjectProps(name);
   return true;
}

double FC_Bezier(const double p0, const double p1, const double p2, const double p3, const double u)
{
   double v = 1.0 - u;
   return v*v*v*p0 + 3.0*v*v*u*p1 + 3.0*v*u*u*p2 + u*u*u*p3;
}

void FC_DrawBezierCurve(const string prefix,
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
   int n = MathMax(8, segments);
   datetime prev_t = t0;
   double prev_p = p0;
   for(int i=1; i<=n; i++)
   {
      double u = (double)i / (double)n;
      datetime next_t = (datetime)MathRound(FC_Bezier((double)((long)t0),
                                                      (double)((long)c1t),
                                                      (double)((long)c2t),
                                                      (double)((long)t3),
                                                      u));
      double next_p = FC_Bezier(p0, c1p, c2p, p3, u);
      FC_DrawTrendRaw(prefix + IntegerToString(i), prev_t, prev_p, next_t, next_p, clr, width, STYLE_SOLID);
      prev_t = next_t;
      prev_p = next_p;
   }
}

color FC_EventRenderColor(const FC_FlagEvent &e,
                          const color f1_pending,
                          const color f1_confirmed,
                          const color f2_pending,
                          const color f2_confirmed)
{
   if(e.level == FC_LEVEL_F2)
      return e.status == FC_STATUS_CONFIRMED ? f2_confirmed : f2_pending;
   return e.status == FC_STATUS_CONFIRMED ? f1_confirmed : f1_pending;
}

void FC_DrawFlagBody(const FC_FlagEvent &e, const string prefix, const color clr, const int width, const int curve_segments)
{
   bool bullish = (e.direction == FC_DIR_BULLISH);
   int sec = PeriodSeconds(_Period);
   if(sec <= 0) sec = 60;

   // Body contract: origin -> leg1 straight; leg1 -> waist -> leg2 curved.
   FC_DrawTrendRaw(prefix + "L0", e.origin.time, e.origin.price, e.leg1.time, e.leg1.price, clr, width, STYLE_SOLID);

   int dt_lw = (int)(e.waist.time - e.leg1.time);
   if(dt_lw <= 0) dt_lw = sec * 4;
   double h_left = MathAbs(e.leg1.price - e.waist.price);
   if(h_left <= 0.0) h_left = 60.0 * _Point;

   datetime c1t = e.leg1.time + (datetime)MathMax(1, (int)(dt_lw * 0.34));
   datetime c2t = e.waist.time - (datetime)MathMax(1, (int)(dt_lw * 0.18));
   double c1p = bullish ? e.leg1.price - 0.40 * h_left : e.leg1.price + 0.40 * h_left;
   double c2p = bullish ? e.waist.price + 0.12 * h_left : e.waist.price - 0.12 * h_left;
   FC_DrawBezierCurve(prefix + "A", e.leg1.time, e.leg1.price, c1t, c1p, c2t, c2p, e.waist.time, e.waist.price, clr, width, curve_segments);

   int dt_wl2 = (int)(e.leg2.time - e.waist.time);
   if(dt_wl2 <= 0) dt_wl2 = sec * 4;
   double h_right = MathAbs(e.leg2.price - e.waist.price);
   if(h_right <= 0.0) h_right = 60.0 * _Point;

   datetime c3t = e.waist.time + (datetime)MathMax(1, (int)(dt_wl2 * 0.26));
   datetime c4t = e.leg2.time - (datetime)MathMax(1, (int)(dt_wl2 * 0.16));
   double c3p = bullish ? e.waist.price + 0.12 * h_right : e.waist.price - 0.12 * h_right;
   double c4p = bullish ? e.leg2.price - 0.14 * h_right : e.leg2.price + 0.14 * h_right;
   FC_DrawBezierCurve(prefix + "B", e.waist.time, e.waist.price, c3t, c3p, c4t, c4p, e.leg2.time, e.leg2.price, clr, width, curve_segments);
}

void FC_DrawFlagLabels(const FC_FlagEvent &e,
                       const string prefix,
                       const color clr,
                       const bool show_flag_label,
                       const bool show_internal_labels,
                       const int flag_font,
                       const int internal_font)
{
   bool bullish = (e.direction == FC_DIR_BULLISH);
   double h = MathMax(MathAbs(e.leg1.price - e.waist.price), MathAbs(e.leg2.price - e.waist.price));
   if(h <= 0.0) h = 60.0 * _Point;

   if(show_flag_label)
   {
      string label = FC_LevelToString(e.level);
      datetime anchor_t = e.leg2.time;
      double anchor_p = e.leg2.price;
      if(e.status == FC_STATUS_CONFIRMED && e.confirm_index >= 0)
      {
         anchor_t = e.confirm_time;
         anchor_p = e.confirm_price;
      }
      double off = MathMax(0.18 * h, 30.0 * _Point);
      double p = bullish ? anchor_p + off : anchor_p - off;
      FC_DrawTextRaw(prefix + "F", anchor_t, p, label, clr, flag_font, bullish ? ANCHOR_LEFT_LOWER : ANCHOR_LEFT_UPPER);
   }

   // Internal 1/2 are numeric labels only. No post-leg2 lines are drawn.
   if(show_internal_labels && e.has_n1 && e.n1.index >= 0)
   {
      double off = MathMax(0.08 * h, 15.0 * _Point);
      double p = bullish ? e.n1.price - off : e.n1.price + off;
      FC_DrawTextRaw(prefix + "I1", e.n1.time, p, "1", clr, internal_font, ANCHOR_CENTER);
   }
   if(show_internal_labels && e.has_n2 && e.n2.index >= 0)
   {
      double off = MathMax(0.08 * h, 15.0 * _Point);
      double p = bullish ? e.n2.price - off : e.n2.price + off;
      FC_DrawTextRaw(prefix + "I2", e.n2.time, p, "2", clr, internal_font, ANCHOR_CENTER);
   }
}

int FC_DrawFlags(const FC_FlagEvent &events[],
                 const int max_events,
                 const bool draw_f1,
                 const bool draw_f2,
                 const bool draw_only_confirmed,
                 const string prefix,
                 const color f1_pending,
                 const color f1_confirmed,
                 const color f2_pending,
                 const color f2_confirmed,
                 const int line_width,
                 const int curve_segments,
                 const bool show_flag_label,
                 const bool show_internal_labels,
                 const int flag_font,
                 const int internal_font)
{
   FC_DeleteObjectsByPrefix(prefix);
   int drawn = 0;
   int total = ArraySize(events);

   for(int i=total-1; i>=0 && drawn<max_events; i--)
   {
      if(events[i].status == FC_STATUS_INVALIDATED) continue;
      if(draw_only_confirmed && events[i].status != FC_STATUS_CONFIRMED) continue;
      if(events[i].level == FC_LEVEL_F1 && !draw_f1) continue;
      if(events[i].level == FC_LEVEL_F2 && !draw_f2) continue;

      color clr = FC_EventRenderColor(events[i], f1_pending, f1_confirmed, f2_pending, f2_confirmed);
      string p = prefix + FC_LevelToString(events[i].level) + "_" + IntegerToString(drawn) + "_";
      FC_DrawFlagBody(events[i], p, clr, line_width, curve_segments);
      FC_DrawFlagLabels(events[i], p, clr, show_flag_label, show_internal_labels, flag_font, internal_font);
      drawn++;
   }

   ChartRedraw(0);
   return drawn;
}

#endif
