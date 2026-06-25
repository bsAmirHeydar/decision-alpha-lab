#property strict
#property indicator_separate_window
#property indicator_minimum 0
#property indicator_maximum 100
#property indicator_buffers 8
#property indicator_plots   8
#property indicator_level1 20.0
#property indicator_level2 50.0
#property indicator_level3 80.0
#property indicator_levelcolor clrDimGray
#property indicator_levelstyle STYLE_DOT
#property indicator_levelwidth 1

#property indicator_label1 "A1"
#property indicator_type1  DRAW_LINE
#property indicator_color1 clrLime
#property indicator_style1 STYLE_SOLID
#property indicator_width1 2

#property indicator_label2 "A2"
#property indicator_type2  DRAW_LINE
#property indicator_color2 clrTomato
#property indicator_style2 STYLE_SOLID
#property indicator_width2 2

#property indicator_label3 "A3"
#property indicator_type3  DRAW_LINE
#property indicator_color3 clrAqua
#property indicator_style3 STYLE_SOLID
#property indicator_width3 1

#property indicator_label4 "A4"
#property indicator_type4  DRAW_LINE
#property indicator_color4 clrOrange
#property indicator_style4 STYLE_SOLID
#property indicator_width4 1

#property indicator_label5 "A5"
#property indicator_type5  DRAW_LINE
#property indicator_color5 clrMagenta
#property indicator_style5 STYLE_DOT
#property indicator_width5 1

#property indicator_label6 "A6"
#property indicator_type6  DRAW_LINE
#property indicator_color6 clrDodgerBlue
#property indicator_style6 STYLE_DOT
#property indicator_width6 1

#property indicator_label7 "A7"
#property indicator_type7  DRAW_LINE
#property indicator_color7 clrSilver
#property indicator_style7 STYLE_DOT
#property indicator_width7 1

#property indicator_label8 "A8"
#property indicator_type8  DRAW_LINE
#property indicator_color8 clrGold
#property indicator_style8 STYLE_DOT
#property indicator_width8 1

#property tester_file "astro_GMT3_M1_2026_to_now_mql.csv"
#property tester_file "astro\\astro_GMT3_M1_2026_to_now_mql.csv"

#include <Research/DAL_AstroMapTypes.mqh>
#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroFractalPathMetrics.mqh>

enum DAL_AstroFractalOscPreset
{
   ASTRO_OSC_RAW_AXES = 0,
   ASTRO_OSC_MACRO_BACKGROUND = 1,
   ASTRO_OSC_REGIME_ENGINE = 2,
   ASTRO_OSC_MOON_MICRO = 3,
   ASTRO_OSC_M1_PATH_QUALITY = 4,
   ASTRO_OSC_COMPACT_JACKPOT = 5
};

input string                    InpAstroCsvFile         = "astro_GMT3_M1_2026_to_now_mql.csv";
input double                    InpBrokerGmtOffsetHours = 0.0;
input bool                      InpRequireExactBarTime  = true;
input int                       InpMaxBarsToProcess     = 10000;
input DAL_AstroFractalOscPreset InpPreset               = ASTRO_OSC_M1_PATH_QUALITY;
input bool                      InpShowDiagnosticsLine  = true;

double g_b0[];
double g_b1[];
double g_b2[];
double g_b3[];
double g_b4[];
double g_b5[];
double g_b6[];
double g_b7[];

DAL_AstroMapStore g_store;
bool g_loaded = false;
string g_status = "";

void DAL_AstroFO_SetPlot(const int plot, const string label, const color clr, const ENUM_LINE_STYLE style, const int width, const bool visible = true)
{
   PlotIndexSetString(plot, PLOT_LABEL, label);
   PlotIndexSetInteger(plot, PLOT_LINE_COLOR, clr);
   PlotIndexSetInteger(plot, PLOT_LINE_STYLE, style);
   PlotIndexSetInteger(plot, PLOT_LINE_WIDTH, width);
   PlotIndexSetInteger(plot, PLOT_DRAW_TYPE, visible ? DRAW_LINE : DRAW_NONE);
   PlotIndexSetDouble(plot, PLOT_EMPTY_VALUE, EMPTY_VALUE);
   PlotIndexSetInteger(plot, PLOT_SHOW_DATA, true);
}

void DAL_AstroFO_SetPresetPlots()
{
   if(InpPreset == ASTRO_OSC_RAW_AXES)
   {
      IndicatorSetString(INDICATOR_SHORTNAME, "EXP0013 Astro RAW Axes");
      DAL_AstroFO_SetPlot(0, "Impulse",    clrLime,       STYLE_SOLID, 2);
      DAL_AstroFO_SetPlot(1, "Friction",   clrTomato,     STYLE_SOLID, 2);
      DAL_AstroFO_SetPlot(2, "Flow",       clrAqua,       STYLE_SOLID, 1);
      DAL_AstroFO_SetPlot(3, "Pressure",   clrOrange,     STYLE_SOLID, 1);
      DAL_AstroFO_SetPlot(4, "Transition", clrMagenta,    STYLE_DOT,   1);
      DAL_AstroFO_SetPlot(5, "MoonTempo",  clrDodgerBlue, STYLE_DOT,   1);
      DAL_AstroFO_SetPlot(6, "SaturnDrag", clrSilver,     STYLE_DOT,   1);
      DAL_AstroFO_SetPlot(7, "NoData",     clrDimGray,    STYLE_DOT,   1, InpShowDiagnosticsLine);
      return;
   }

   if(InpPreset == ASTRO_OSC_MACRO_BACKGROUND)
   {
      IndicatorSetString(INDICATOR_SHORTNAME, "EXP0013 Astro MACRO Background");
      DAL_AstroFO_SetPlot(0, "MacroFlow",       clrAqua,    STYLE_SOLID, 2);
      DAL_AstroFO_SetPlot(1, "MacroDrag",       clrTomato,  STYLE_SOLID, 2);
      DAL_AstroFO_SetPlot(2, "MacroPressure",   clrOrange,  STYLE_SOLID, 1);
      DAL_AstroFO_SetPlot(3, "MacroTransition", clrMagenta, STYLE_SOLID, 1);
      DAL_AstroFO_SetPlot(4, "Expansion",       clrLime,    STYLE_DOT,   1);
      DAL_AstroFO_SetPlot(5, "Compression",     clrSilver,  STYLE_DOT,   1);
      DAL_AstroFO_SetPlot(6, "OuterStation",    clrGold,    STYLE_DOT,   1);
      DAL_AstroFO_SetPlot(7, "StructuralBias",  clrWhite,   STYLE_DOT,   1);
      return;
   }

   if(InpPreset == ASTRO_OSC_REGIME_ENGINE)
   {
      IndicatorSetString(INDICATOR_SHORTNAME, "EXP0013 Astro REGIME Engine");
      DAL_AstroFO_SetPlot(0, "MarsImpulse",      clrLime,       STYLE_SOLID, 2);
      DAL_AstroFO_SetPlot(1, "MarsCleanImpulse", clrGreenYellow, STYLE_SOLID, 2);
      DAL_AstroFO_SetPlot(2, "MarsSatFriction",  clrTomato,     STYLE_SOLID, 1);
      DAL_AstroFO_SetPlot(3, "MercuryNoise",     clrOrange,     STYLE_SOLID, 1);
      DAL_AstroFO_SetPlot(4, "JupiterSupport",   clrAqua,       STYLE_DOT,   1);
      DAL_AstroFO_SetPlot(5, "SaturnResistance", clrSilver,     STYLE_DOT,   1);
      DAL_AstroFO_SetPlot(6, "VenusMarsCohesion",clrViolet,     STYLE_DOT,   1);
      DAL_AstroFO_SetPlot(7, "NoData",           clrDimGray,    STYLE_DOT,   1, InpShowDiagnosticsLine);
      return;
   }

   if(InpPreset == ASTRO_OSC_MOON_MICRO)
   {
      IndicatorSetString(INDICATOR_SHORTNAME, "EXP0013 Astro MOON Micro M1");
      DAL_AstroFO_SetPlot(0, "MoonTempo",      clrDodgerBlue, STYLE_SOLID, 2);
      DAL_AstroFO_SetPlot(1, "MoonPressure",   clrOrange,     STYLE_SOLID, 2);
      DAL_AstroFO_SetPlot(2, "MoonFlow",       clrAqua,       STYLE_SOLID, 1);
      DAL_AstroFO_SetPlot(3, "MoonDrag",       clrTomato,     STYLE_SOLID, 1);
      DAL_AstroFO_SetPlot(4, "MoonBoundary",   clrMagenta,    STYLE_DOT,   1);
      DAL_AstroFO_SetPlot(5, "MoonOOB",        clrGold,       STYLE_DOT,   1);
      DAL_AstroFO_SetPlot(6, "MicroNoise",     clrRed,        STYLE_DOT,   1);
      DAL_AstroFO_SetPlot(7, "MicroClean",     clrLime,       STYLE_DOT,   1);
      return;
   }

   if(InpPreset == ASTRO_OSC_COMPACT_JACKPOT)
   {
      IndicatorSetString(INDICATOR_SHORTNAME, "EXP0013 Astro COMPACT Jackpot Path");
      DAL_AstroFO_SetPlot(0, "M1CleanWindow", clrLime,    STYLE_SOLID, 3);
      DAL_AstroFO_SetPlot(1, "M1DirtyWindow", clrTomato,  STYLE_SOLID, 2);
      DAL_AstroFO_SetPlot(2, "BreakoutFT",    clrAqua,    STYLE_SOLID, 1);
      DAL_AstroFO_SetPlot(3, "PullbackRisk",  clrOrange,  STYLE_SOLID, 1);
      DAL_AstroFO_SetPlot(4, "CleanImpulse",  clrGreenYellow, STYLE_DOT, 1);
      DAL_AstroFO_SetPlot(5, "ChopRisk",      clrMagenta, STYLE_DOT,   1);
      DAL_AstroFO_SetPlot(6, "NoData",        clrDimGray, STYLE_DOT,   1, InpShowDiagnosticsLine);
      DAL_AstroFO_SetPlot(7, "Hidden",        clrGray,    STYLE_DOT,   1, false);
      return;
   }

   // Default: M1 path quality.
   IndicatorSetString(INDICATOR_SHORTNAME, "EXP0013 Astro M1 PATH Quality");
   DAL_AstroFO_SetPlot(0, "CleanPath",    clrLime,       STYLE_SOLID, 2);
   DAL_AstroFO_SetPlot(1, "CleanImpulse", clrGreenYellow, STYLE_SOLID, 2);
   DAL_AstroFO_SetPlot(2, "SmoothCont",   clrAqua,       STYLE_SOLID, 1);
   DAL_AstroFO_SetPlot(3, "BreakoutFT",   clrDodgerBlue, STYLE_SOLID, 1);
   DAL_AstroFO_SetPlot(4, "PullbackRisk", clrOrangeRed,  STYLE_DOT,   1);
   DAL_AstroFO_SetPlot(5, "ChopRisk",     clrMagenta,    STYLE_DOT,   1);
   DAL_AstroFO_SetPlot(6, "M1CleanWindow",clrGold,       STYLE_DOT,   1);
   DAL_AstroFO_SetPlot(7, "M1DirtyWindow",clrTomato,     STYLE_DOT,   1);
}

void DAL_AstroFO_ResetBuffers(const int rates_total)
{
   for(int i = 0; i < rates_total; i++)
   {
      g_b0[i] = EMPTY_VALUE;
      g_b1[i] = EMPTY_VALUE;
      g_b2[i] = EMPTY_VALUE;
      g_b3[i] = EMPTY_VALUE;
      g_b4[i] = EMPTY_VALUE;
      g_b5[i] = EMPTY_VALUE;
      g_b6[i] = EMPTY_VALUE;
      g_b7[i] = EMPTY_VALUE;
   }
}

void DAL_AstroFO_SetNoData(const int i)
{
   if(InpShowDiagnosticsLine)
   {
      g_b0[i] = 0.0;
      g_b1[i] = EMPTY_VALUE;
      g_b2[i] = EMPTY_VALUE;
      g_b3[i] = EMPTY_VALUE;
      g_b4[i] = EMPTY_VALUE;
      g_b5[i] = EMPTY_VALUE;
      g_b6[i] = EMPTY_VALUE;
      g_b7[i] = EMPTY_VALUE;
   }
}

void DAL_AstroFO_AssignPreset(const int i, const DAL_AstroFractalMetrics &f)
{
   if(InpPreset == ASTRO_OSC_RAW_AXES)
   {
      g_b0[i] = f.raw_impulse;
      g_b1[i] = f.raw_friction;
      g_b2[i] = f.raw_flow;
      g_b3[i] = f.raw_pressure;
      g_b4[i] = f.raw_transition;
      g_b5[i] = f.raw_moon_tempo;
      g_b6[i] = f.raw_saturn_drag;
      g_b7[i] = EMPTY_VALUE;
      return;
   }

   if(InpPreset == ASTRO_OSC_MACRO_BACKGROUND)
   {
      g_b0[i] = f.macro_flow;
      g_b1[i] = f.macro_drag;
      g_b2[i] = f.macro_pressure;
      g_b3[i] = f.macro_transition;
      g_b4[i] = f.macro_expansion;
      g_b5[i] = f.macro_compression;
      g_b6[i] = f.outer_station_risk;
      g_b7[i] = f.structural_bias;
      return;
   }

   if(InpPreset == ASTRO_OSC_REGIME_ENGINE)
   {
      g_b0[i] = f.mars_impulse;
      g_b1[i] = f.mars_clean_impulse;
      g_b2[i] = f.mars_saturn_friction;
      g_b3[i] = f.mercury_noise;
      g_b4[i] = f.jupiter_support;
      g_b5[i] = f.saturn_resistance;
      g_b6[i] = f.venus_mars_cohesion;
      g_b7[i] = EMPTY_VALUE;
      return;
   }

   if(InpPreset == ASTRO_OSC_MOON_MICRO)
   {
      g_b0[i] = f.moon_tempo;
      g_b1[i] = f.moon_pressure;
      g_b2[i] = f.moon_flow;
      g_b3[i] = f.moon_drag;
      g_b4[i] = f.moon_boundary;
      g_b5[i] = f.moon_oob_intensity;
      g_b6[i] = f.micro_noise;
      g_b7[i] = f.micro_cleanliness;
      return;
   }

   if(InpPreset == ASTRO_OSC_COMPACT_JACKPOT)
   {
      g_b0[i] = f.m1_clean_window;
      g_b1[i] = f.m1_dirty_window;
      g_b2[i] = f.breakout_followthrough;
      g_b3[i] = f.pullback_risk;
      g_b4[i] = f.clean_impulse;
      g_b5[i] = f.chop_risk;
      g_b6[i] = EMPTY_VALUE;
      g_b7[i] = EMPTY_VALUE;
      return;
   }

   g_b0[i] = f.clean_path;
   g_b1[i] = f.clean_impulse;
   g_b2[i] = f.smooth_continuation;
   g_b3[i] = f.breakout_followthrough;
   g_b4[i] = f.pullback_risk;
   g_b5[i] = f.chop_risk;
   g_b6[i] = f.m1_clean_window;
   g_b7[i] = f.m1_dirty_window;
}

int OnInit()
{
   SetIndexBuffer(0, g_b0, INDICATOR_DATA);
   SetIndexBuffer(1, g_b1, INDICATOR_DATA);
   SetIndexBuffer(2, g_b2, INDICATOR_DATA);
   SetIndexBuffer(3, g_b3, INDICATOR_DATA);
   SetIndexBuffer(4, g_b4, INDICATOR_DATA);
   SetIndexBuffer(5, g_b5, INDICATOR_DATA);
   SetIndexBuffer(6, g_b6, INDICATOR_DATA);
   SetIndexBuffer(7, g_b7, INDICATOR_DATA);

   ArraySetAsSeries(g_b0, true);
   ArraySetAsSeries(g_b1, true);
   ArraySetAsSeries(g_b2, true);
   ArraySetAsSeries(g_b3, true);
   ArraySetAsSeries(g_b4, true);
   ArraySetAsSeries(g_b5, true);
   ArraySetAsSeries(g_b6, true);
   ArraySetAsSeries(g_b7, true);

   IndicatorSetInteger(INDICATOR_DIGITS, 1);
   DAL_AstroFO_SetPresetPlots();

   g_loaded = DAL_AstroMapStore_LoadExcelCsv(g_store, InpAstroCsvFile, InpBrokerGmtOffsetHours, 1);
   if(!g_loaded)
   {
      g_status = "CSV NOT LOADED | file=" + InpAstroCsvFile;
      Print("EXP0013_AstroFractalOscillator | ", g_status);
      IndicatorSetString(INDICATOR_SHORTNAME, "EXP0013 Astro Fractal Oscillator [CSV NOT LOADED]");
   }
   else
   {
      g_status = "CSV LOADED | rows=" + IntegerToString(g_store.row_count) + " | source=" + g_store.source_file;
      Print("EXP0013_AstroFractalOscillator | ", g_status);
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
      DAL_AstroFO_ResetBuffers(rates_total);

   int bars_to_process = rates_total;
   if(InpMaxBarsToProcess > 0)
      bars_to_process = MathMin(rates_total, InpMaxBarsToProcess);

   if(!g_loaded)
   {
      for(int i = 0; i < bars_to_process; i++)
         DAL_AstroFO_SetNoData(i);
      return rates_total;
   }

   for(int i = bars_to_process - 1; i >= 0; i--)
   {
      DAL_AstroMapRow row;
      if(!DAL_AstroMapStore_FindForCandleOpen(g_store, time[i], row, InpRequireExactBarTime))
      {
         DAL_AstroFO_SetNoData(i);
         continue;
      }

      DAL_AstroFractalMetrics f;
      if(!DAL_AstroFM_Calc(row, f) || !f.valid)
      {
         DAL_AstroFO_SetNoData(i);
         continue;
      }

      DAL_AstroFO_AssignPreset(i, f);
   }

   return rates_total;
}
