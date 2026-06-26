#ifndef __DAL_M0007_F1_RENDERER_MQH__
#define __DAL_M0007_F1_RENDERER_MQH__
#property strict
#include <M0007/DAL_M0007F1Types.mqh>

void M0007_DeleteObjectsByPrefix(const string prefix)
{
   for(int i=ObjectsTotal(0, -1, -1)-1; i>=0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(StringFind(name, prefix) == 0)
         ObjectDelete(0, name);
   }
}

void M0007_DeleteBrokenDefaultTextObjects()
{
   for(int i=ObjectsTotal(0, -1, -1)-1; i>=0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(ObjectGetInteger(0, name, OBJPROP_TYPE) != OBJ_TEXT)
         continue;
      string displayed = ObjectGetString(0, name, OBJPROP_TEXT);
      if(displayed == "Text")
         ObjectDelete(0, name);
   }
}

void M0007_SetCommonObjectProps(const string name)
{
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
}

bool M0007_DrawTrendRaw(const string name,
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
      Print("M0007 renderer: trend create failed name=", name, " err=", GetLastError());
      return false;
   }
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, false);
   ObjectSetInteger(0, name, OBJPROP_RAY_LEFT, false);
   M0007_SetCommonObjectProps(name);
   return true;
}

bool M0007_DrawTextRaw(const string name,
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
      Print("M0007 renderer: text create failed name=", name, " value=", value, " err=", GetLastError());
      return false;
   }
   ObjectSetString(0, name, OBJPROP_TEXT, value);
   ObjectSetString(0, name, OBJPROP_FONT, "Arial Bold");
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetInteger(0, name, OBJPROP_ANCHOR, anchor);
   M0007_SetCommonObjectProps(name);
   return true;
}

double M0007_Bezier(const double p0, const double p1, const double p2, const double p3, const double u)
{
   double v = 1.0 - u;
   return v*v*v*p0 + 3.0*v*v*u*p1 + 3.0*v*u*u*p2 + u*u*u*p3;
}

void M0007_DrawBezierCurve(const string prefix,
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
      datetime next_t = (datetime)MathRound(M0007_Bezier((double)((long)t0), (double)((long)c1t), (double)((long)c2t), (double)((long)t3), u));
      double next_p = M0007_Bezier(p0, c1p, c2p, p3, u);
      M0007_DrawTrendRaw(prefix + IntegerToString(i), prev_t, prev_p, next_t, next_p, clr, width, STYLE_SOLID);
      prev_t = next_t;
      prev_p = next_p;
   }
}

color M0007_EventRenderColor(const M0007_F1Event &e,
                             const color bullish_pending_color,
                             const color bearish_pending_color,
                             const color bullish_confirmed_color,
                             const color bearish_confirmed_color)
{
   if(e.status == M0007_STATUS_CONFIRMED)
      return (e.direction == M0007_DIR_BULLISH ? bullish_confirmed_color : bearish_confirmed_color);
   return (e.direction == M0007_DIR_BULLISH ? bullish_pending_color : bearish_pending_color);
}

void M0007_DrawF1Path(const M0007_F1Event &e, const string p, const color clr)
{
   bool bullish = (e.direction == M0007_DIR_BULLISH);
   int sec = PeriodSeconds(_Period);
   if(sec <= 0) sec = 60;

   // Start -> Leg1 straight.
   M0007_DrawTrendRaw(p + "L0", e.Start.time, e.Start.price, e.H1.time, e.H1.price, clr, 2, STYLE_SOLID);

   // Leg1 -> Waist smooth curve.
   int dt_hw = (int)(e.W.time - e.H1.time);
   if(dt_hw <= 0) dt_hw = sec * 4;
   double h_left = MathAbs(e.H1.price - e.W.price);
   if(h_left <= 0.0) h_left = 60.0 * _Point;
   datetime c1t = e.H1.time + (datetime)MathMax(1, (int)(dt_hw * 0.33));
   datetime c2t = e.W.time  - (datetime)MathMax(1, (int)(dt_hw * 0.20));
   double c1p = bullish ? e.H1.price - 0.42 * h_left : e.H1.price + 0.42 * h_left;
   double c2p = bullish ? e.W.price  + 0.10 * h_left : e.W.price  - 0.10 * h_left;
   M0007_DrawBezierCurve(p + "A", e.H1.time, e.H1.price, c1t, c1p, c2t, c2p, e.W.time, e.W.price, clr, 2, 10);

   // Waist -> Leg2 smooth curve.
   int dt_wh = (int)(e.H2.time - e.W.time);
   if(dt_wh <= 0) dt_wh = sec * 4;
   double h_right = MathAbs(e.H2.price - e.W.price);
   if(h_right <= 0.0) h_right = 60.0 * _Point;
   datetime c3t = e.W.time  + (datetime)MathMax(1, (int)(dt_wh * 0.28));
   datetime c4t = e.H2.time - (datetime)MathMax(1, (int)(dt_wh * 0.24));
   double c3p = bullish ? e.W.price  + 0.10 * h_right : e.W.price  - 0.10 * h_right;
   double c4p = bullish ? e.H2.price - 0.32 * h_right : e.H2.price + 0.32 * h_right;
   M0007_DrawBezierCurve(p + "B", e.W.time, e.W.price, c3t, c3p, c4t, c4p, e.H2.time, e.H2.price, clr, 2, 10);

   // Extend the visible path after Leg2 into internal 1/2 and final confirmation when available.
   if(e.has_internal_1 && e.N1.index >= 0)
      M0007_DrawTrendRaw(p + "L1", e.H2.time, e.H2.price, e.N1.time, e.N1.price, clr, 2, STYLE_SOLID);
   if(e.has_internal_1 && e.has_internal_2 && e.N1.index >= 0 && e.N2.index >= 0)
      M0007_DrawTrendRaw(p + "L2", e.N1.time, e.N1.price, e.N2.time, e.N2.price, clr, 2, STYLE_SOLID);

   datetime end_t = 0; double end_p = 0.0;
   if(e.status == M0007_STATUS_CONFIRMED && e.confirm_index >= 0)
   {
      end_t = e.confirm_time; end_p = e.confirm_price;
      if(e.has_internal_2 && e.N2.index >= 0)
         M0007_DrawTrendRaw(p + "L3", e.N2.time, e.N2.price, end_t, end_p, clr, 2, STYLE_SOLID);
      else if(e.has_internal_1 && e.N1.index >= 0)
         M0007_DrawTrendRaw(p + "L3", e.N1.time, e.N1.price, end_t, end_p, clr, 2, STYLE_SOLID);
      else
         M0007_DrawTrendRaw(p + "L3", e.H2.time, e.H2.price, end_t, end_p, clr, 2, STYLE_SOLID);
   }
}

void M0007_DrawF1Labels(const M0007_F1Event &e,
                        const string p,
                        const color clr,
                        const bool show_internal_counts,
                        const bool show_f1_label)
{
   bool bullish = (e.direction == M0007_DIR_BULLISH);
   double h = MathMax(MathAbs(e.H1.price - e.W.price), MathAbs(e.H2.price - e.W.price));
   if(h <= 0.0) h = 60.0 * _Point;

   if(show_f1_label)
   {
      datetime anchor_t = e.H2.time;
      double anchor_p = e.H2.price;
      if(e.status == M0007_STATUS_CONFIRMED && e.confirm_index >= 0)
      {
         anchor_t = e.confirm_time;
         anchor_p = e.confirm_price;
      }
      double f1_offset = MathMax(0.18 * h, 30.0 * _Point);
      double f1_p = bullish ? anchor_p + f1_offset : anchor_p - f1_offset;
      M0007_DrawTextRaw(p + "F", anchor_t, f1_p, "F1", clr, 16, bullish ? ANCHOR_LEFT_LOWER : ANCHOR_LEFT_UPPER);
   }

   if(show_internal_counts && e.has_internal_1 && e.N1.index >= 0)
   {
      double dy1 = MathMax(0.08 * h, 15.0 * _Point);
      double p1 = bullish ? e.N1.price - dy1 : e.N1.price + dy1;
      M0007_DrawTextRaw(p + "I1", e.N1.time, p1, "1", clr, 12, ANCHOR_CENTER);
   }
   if(show_internal_counts && e.has_internal_2 && e.N2.index >= 0)
   {
      double dy2 = MathMax(0.08 * h, 15.0 * _Point);
      double p2 = bullish ? e.N2.price - dy2 : e.N2.price + dy2;
      M0007_DrawTextRaw(p + "I2", e.N2.time, p2, "2", clr, 12, ANCHOR_CENTER);
   }
}

void M0007_DrawEvent(const M0007_F1Event &e,
                     const string prefix,
                     const int event_number,
                     const bool show_internal_counts,
                     const bool show_f1_label,
                     const color bullish_pending_color,
                     const color bearish_pending_color,
                     const color bullish_confirmed_color,
                     const color bearish_confirmed_color)
{
   string p = prefix + IntegerToString(event_number) + "_";
   color clr = M0007_EventRenderColor(e,
                                      bullish_pending_color,
                                      bearish_pending_color,
                                      bullish_confirmed_color,
                                      bearish_confirmed_color);
   M0007_DrawF1Path(e, p, clr);
   M0007_DrawF1Labels(e, p, clr, show_internal_counts, show_f1_label);
}

int M0007_DrawEvents(const M0007_F1Event &events[],
                     const int max_events,
                     const bool draw_only_confirmed,
                     const string prefix,
                     const bool show_internal_counts,
                     const bool show_f1_label,
                     const color bullish_pending_color,
                     const color bearish_pending_color,
                     const color bullish_confirmed_color,
                     const color bearish_confirmed_color)
{
   M0007_DeleteObjectsByPrefix(prefix);
   M0007_DeleteBrokenDefaultTextObjects();
   int drawn = 0;
   int total = ArraySize(events);
   for(int i=total-1; i>=0 && drawn<max_events; i--)
   {
      if(events[i].status == M0007_STATUS_INVALIDATED)
         continue;
      if(draw_only_confirmed && events[i].status != M0007_STATUS_CONFIRMED)
         continue;
      M0007_DrawEvent(events[i], prefix, drawn, show_internal_counts, show_f1_label,
                      bullish_pending_color, bearish_pending_color,
                      bullish_confirmed_color, bearish_confirmed_color);
      drawn++;
   }
   ChartRedraw(0);
   return drawn;
}

#endif
