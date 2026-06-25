#property strict
#property indicator_separate_window
#property indicator_minimum 0
#property indicator_maximum 100
#property indicator_buffers 7
#property indicator_plots   7
#property indicator_level1 25.0
#property indicator_level2 50.0
#property indicator_level3 75.0
#property indicator_levelcolor clrDimGray
#property indicator_levelstyle STYLE_DOT
#property indicator_levelwidth 1

// MQL5 plot properties must use indicator_labelN / indicator_typeN / indicator_colorN.
// The non-standard #property plotN syntax is intentionally not used.
#property indicator_label1  "Flow"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrAqua
#property indicator_style1  STYLE_SOLID
#property indicator_width1  2

#property indicator_label2  "Impulse"
#property indicator_type2   DRAW_LINE
#property indicator_color2  clrLime
#property indicator_style2  STYLE_SOLID
#property indicator_width2  2

#property indicator_label3  "Friction"
#property indicator_type3   DRAW_LINE
#property indicator_color3  clrTomato
#property indicator_style3  STYLE_SOLID
#property indicator_width3  2

#property indicator_label4  "Pressure"
#property indicator_type4   DRAW_LINE
#property indicator_color4  clrOrange
#property indicator_style4  STYLE_SOLID
#property indicator_width4  2

#property indicator_label5  "Transition"
#property indicator_type5   DRAW_LINE
#property indicator_color5  clrMagenta
#property indicator_style5  STYLE_DASH
#property indicator_width5  1

#property indicator_label6  "MoonTempo"
#property indicator_type6   DRAW_LINE
#property indicator_color6  clrDodgerBlue
#property indicator_style6  STYLE_DASH
#property indicator_width6  1

#property indicator_label7  "SaturnDrag"
#property indicator_type7   DRAW_LINE
#property indicator_color7  clrSilver
#property indicator_style7  STYLE_DASH
#property indicator_width7  1

#property tester_file "astro_GMT3_M1_2026_to_now_mql.csv"
#property tester_file "astro\\astro_GMT3_M1_2026_to_now_mql.csv"

#include <Research/DAL_AstroMapTypes.mqh>
#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroPathCleanlinessMetrics.mqh>

input string InpAstroCsvFile            = "astro_GMT3_M1_2026_to_now_mql.csv";
input double InpBrokerGmtOffsetHours    = 0.0;
input bool   InpRequireExactBarTime     = true;
input int    InpMaxBarsToProcess        = 5000;
input bool   InpShowFlow                = true;
input bool   InpShowImpulse             = true;
input bool   InpShowFriction            = true;
input bool   InpShowPressure            = true;
input bool   InpShowTransition          = false;
input bool   InpShowMoonTempo           = false;
input bool   InpShowSaturnDrag          = false;

DAL_AstroMapStore g_store;
bool g_loaded = false;

double g_flow[];
double g_impulse[];
double g_friction[];
double g_pressure[];
double g_transition[];
double g_moon_tempo[];
double g_saturn_drag[];

void DAL_AstroRawOsc_SetPlot(
   const int plot,
   const string label,
   const color clr,
   const ENUM_LINE_STYLE style,
   const int width,
   const bool visible
)
{
   PlotIndexSetString(plot, PLOT_LABEL, label);
   PlotIndexSetInteger(plot, PLOT_LINE_COLOR, clr);
   PlotIndexSetInteger(plot, PLOT_LINE_STYLE, style);
   PlotIndexSetInteger(plot, PLOT_LINE_WIDTH, width);
   PlotIndexSetInteger(plot, PLOT_DRAW_TYPE, visible ? DRAW_LINE : DRAW_NONE);
   PlotIndexSetDouble(plot, PLOT_EMPTY_VALUE, EMPTY_VALUE);
   PlotIndexSetInteger(plot, PLOT_SHOW_DATA, visible);
}

void DAL_AstroRawOsc_SetEmptyAt(const int i)
{
   g_flow[i]        = EMPTY_VALUE;
   g_impulse[i]     = EMPTY_VALUE;
   g_friction[i]    = EMPTY_VALUE;
   g_pressure[i]    = EMPTY_VALUE;
   g_transition[i]  = EMPTY_VALUE;
   g_moon_tempo[i]  = EMPTY_VALUE;
   g_saturn_drag[i] = EMPTY_VALUE;
}

void DAL_AstroRawOsc_ResetBuffers(const int rates_total)
{
   for(int i = 0; i < rates_total; i++)
      DAL_AstroRawOsc_SetEmptyAt(i);
}

int OnInit()
{
   IndicatorSetString(INDICATOR_SHORTNAME, "EXP0013 Astro Raw Axes Oscillator");
   IndicatorSetInteger(INDICATOR_DIGITS, 1);

   SetIndexBuffer(0, g_flow,        INDICATOR_DATA);
   SetIndexBuffer(1, g_impulse,     INDICATOR_DATA);
   SetIndexBuffer(2, g_friction,    INDICATOR_DATA);
   SetIndexBuffer(3, g_pressure,    INDICATOR_DATA);
   SetIndexBuffer(4, g_transition,  INDICATOR_DATA);
   SetIndexBuffer(5, g_moon_tempo,  INDICATOR_DATA);
   SetIndexBuffer(6, g_saturn_drag, INDICATOR_DATA);

   ArraySetAsSeries(g_flow,        true);
   ArraySetAsSeries(g_impulse,     true);
   ArraySetAsSeries(g_friction,    true);
   ArraySetAsSeries(g_pressure,    true);
   ArraySetAsSeries(g_transition,  true);
   ArraySetAsSeries(g_moon_tempo,  true);
   ArraySetAsSeries(g_saturn_drag, true);

   DAL_AstroRawOsc_SetPlot(0, "Flow",       clrAqua,       STYLE_SOLID, 2, InpShowFlow);
   DAL_AstroRawOsc_SetPlot(1, "Impulse",    clrLime,       STYLE_SOLID, 2, InpShowImpulse);
   DAL_AstroRawOsc_SetPlot(2, "Friction",   clrTomato,     STYLE_SOLID, 2, InpShowFriction);
   DAL_AstroRawOsc_SetPlot(3, "Pressure",   clrOrange,     STYLE_SOLID, 2, InpShowPressure);
   DAL_AstroRawOsc_SetPlot(4, "Transition", clrMagenta,    STYLE_DASH,  1, InpShowTransition);
   DAL_AstroRawOsc_SetPlot(5, "MoonTempo",  clrDodgerBlue, STYLE_DASH,  1, InpShowMoonTempo);
   DAL_AstroRawOsc_SetPlot(6, "SaturnDrag", clrSilver,     STYLE_DASH,  1, InpShowSaturnDrag);

   g_loaded = DAL_AstroMapStore_LoadExcelCsv(
      g_store,
      InpAstroCsvFile,
      InpBrokerGmtOffsetHours,
      1
   );

   if(!g_loaded)
   {
      Print("EXP0013_AstroRawAxesOscillator | astro CSV not loaded | file=", InpAstroCsvFile);
      IndicatorSetString(INDICATOR_SHORTNAME, "EXP0013 Astro Raw Axes Oscillator [CSV NOT LOADED]");
   }

   return INIT_SUCCEEDED;
}

int OnCalculate(
   const int rates_total,
   const int prev_calculated,
   const datetime &time[],
   const double &open[],
   const double &high[],
   const double &low[],
   const double &close[],
   const long &tick_volume[],
   const long &volume[],
   const int &spread[]
)
{
   if(rates_total <= 0)
      return 0;

   if(prev_calculated == 0)
      DAL_AstroRawOsc_ResetBuffers(rates_total);

   if(!g_loaded)
      return rates_total;

   int bars_to_process = rates_total;
   if(InpMaxBarsToProcess > 0)
      bars_to_process = MathMin(rates_total, InpMaxBarsToProcess);

   for(int i = bars_to_process - 1; i >= 0; i--)
   {
      DAL_AstroMapRow row;
      if(!DAL_AstroMapStore_FindForCandleOpen(g_store, time[i], row, InpRequireExactBarTime))
      {
         DAL_AstroRawOsc_SetEmptyAt(i);
         continue;
      }

      DAL_AstroPathMetrics m;
      if(!DAL_AstroPathMetrics_Calc(row, m) || !m.valid)
      {
         DAL_AstroRawOsc_SetEmptyAt(i);
         continue;
      }

      g_flow[i]        = m.flow_score;
      g_impulse[i]     = m.impulse_score;
      g_friction[i]    = m.friction_score;
      g_pressure[i]    = m.pressure_score;
      g_transition[i]  = m.transition_score;
      g_moon_tempo[i]  = m.moon_tempo_score;
      g_saturn_drag[i] = m.saturn_drag_score;
   }

   return rates_total;
}
