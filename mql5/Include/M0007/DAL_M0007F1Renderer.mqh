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

void M0007_DrawSwingArc(const string prefix,
                        const datetime t0,
                        const double p0,
                        const datetime tv,
                        const double pv,
                        const datetime t1,
                        const double p1,
                        const color clr,
                        const int width,
                        const bool bullish,
                        const int segments)
{
   // Part 1: start extreme -> valley/crest.
   int dt0 = (int)(tv - t0);
   if(dt0 <= 0) dt0 = PeriodSeconds(_Period) * 4;
   double h0 = MathAbs(p0 - pv);
   if(h0 <= 0.0) h0 = 60.0 * _Point;

   datetime a1t = t0 + (datetime)MathMax(1, (int)(dt0 * 0.22));
   datetime a2t = tv - (datetime)MathMax(1, (int)(dt0 * 0.18));
   double a1p = bullish ? (p0 - 0.18 * h0) : (p0 + 0.18 * h0);
   double a2p = bullish ? (pv + 0.14 * h0) : (pv - 0.14 * h0);
   M0007_DrawBezierCurve(prefix + "D", t0, p0, a1t, a1p, a2t, a2p, tv, pv, clr, width, segments);

   // Part 2: valley/crest -> rebreak target.
   int dt1 = (int)(t1 - tv);
   if(dt1 <= 0) dt1 = PeriodSeconds(_Period) * 4;
   double h1 = MathAbs(p1 - pv);
   if(h1 <= 0.0) h1 = 60.0 * _Point;

   datetime b1t = tv + (datetime)MathMax(1, (int)(dt1 * 0.28));
   datetime b2t = t1 - (datetime)MathMax(1, (int)(dt1 * 0.20));
   double b1p = bullish ? (pv + 0.16 * h1) : (pv - 0.16 * h1);
   double b2p = bullish ? (p1 - 0.24 * h1) : (p1 + 0.24 * h1);
   M0007_DrawBezierCurve(prefix + "U", tv, pv, b1t, b1p, b2t, b2p, t1, p1, clr, width, segments);
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

   // Segment 1: true start -> top/bottom of leg 1.
   M0007_DrawTrendRaw(p + "L0", e.Start.time, e.Start.price, e.H1.time, e.H1.price, clr, 2, STYLE_SOLID);

   // Segment 2: leg 1 -> waist -> leg 2. Two smooth pieces so the path reaches the leg extreme cleanly.
   int dt_hw = (int)(e.W.time - e.H1.time);
   if(dt_hw <= 0) dt_hw = sec * 4;
   double h_left = MathAbs(e.H1.price - e.W.price);
   if(h_left <= 0.0) h_left = 60.0 * _Point;
   datetime c1t = e.H1.time + (datetime)MathMax(1, (int)(dt_hw * 0.34));
   datetime c2t = e.W.time  - (datetime)MathMax(1, (int)(dt_hw * 0.18));
   double c1p = bullish ? e.H1.price - 0.40 * h_left : e.H1.price + 0.40 * h_left;
   double c2p = bullish ? e.W.price  + 0.12 * h_left : e.W.price  - 0.12 * h_left;
   M0007_DrawBezierCurve(p + "A", e.H1.time, e.H1.price, c1t, c1p, c2t, c2p, e.W.time, e.W.price, clr, 2, 10);

   int dt_wh = (int)(e.H2.time - e.W.time);
   if(dt_wh <= 0) dt_wh = sec * 4;
   double h_right = MathAbs(e.H2.price - e.W.price);
   if(h_right <= 0.0) h_right = 60.0 * _Point;
   datetime c3t = e.W.time  + (datetime)MathMax(1, (int)(dt_wh * 0.26));
   datetime c4t = e.H2.time - (datetime)MathMax(1, (int)(dt_wh * 0.16));
   double c3p = bullish ? e.W.price  + 0.12 * h_right : e.W.price  - 0.12 * h_right;
   double c4p = bullish ? e.H2.price - 0.14 * h_right : e.H2.price + 0.14 * h_right;
   M0007_DrawBezierCurve(p + "B", e.W.time, e.W.price, c3t, c3p, c4t, c4p, e.H2.time, e.H2.price, clr, 2, 10);

   // Segment 3: from end of leg 2 into the open 1/2 area and then back into the leg2 rebreak.
   if(e.has_internal_2 && e.N2.index >= 0)
   {
      datetime end_t = e.N2.time;
      double end_p = e.N2.price;
      if(e.status == M0007_STATUS_CONFIRMED && e.confirm_index >= 0)
      {
         end_t = e.confirm_time;
         end_p = e.confirm_price;
      }
      else if(e.has_internal_1 && e.N1.index >= 0)
      {
         // still open: draw down/up swing into the open internal area and stop at N2.
         end_t = e.N2.time;
         end_p = e.N2.price;
      }
      M0007_DrawSwingArc(p + "C", e.H2.time, e.H2.price, e.N2.time, e.N2.price, end_t, end_p, clr, 2, bullish, 10);
   }
   else if(e.has_internal_1 && e.N1.index >= 0)
   {
      // Partial open path until internal 1 exists.
      int dt = (int)(e.N1.time - e.H2.time);
      if(dt <= 0) dt = sec * 3;
      double hh = MathAbs(e.H2.price - e.N1.price);
      if(hh <= 0.0) hh = 50.0 * _Point;
      datetime d1t = e.H2.time + (datetime)MathMax(1, (int)(dt * 0.30));
      datetime d2t = e.N1.time - (datetime)MathMax(1, (int)(dt * 0.18));
      double d1p = bullish ? e.H2.price - 0.24 * hh : e.H2.price + 0.24 * hh;
      double d2p = bullish ? e.N1.price + 0.14 * hh : e.N1.price - 0.14 * hh;
      M0007_DrawBezierCurve(p + "C", e.H2.time, e.H2.price, d1t, d1p, d2t, d2p, e.N1.time, e.N1.price, clr, 2, 10);
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
