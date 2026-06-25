#property strict
#property description "Decision Alpha Lab - EXP0013 Astro Unified Dashboard EA"
#property description "Research-only visual dashboard. No orders. No iCustom. No indicator loading."
#property tester_file "astro_GMT3_M1_2026_to_now_mql.csv"
#property tester_file "astro\\astro_GMT3_M1_2026_to_now_mql.csv"

#include <Research/DAL_AstroMapTypes.mqh>
#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroPathCleanlinessMetrics.mqh>
#include <Research/DAL_AstroFractalPathMetrics.mqh>

// -----------------------------------------------------------------------------
// EXP0013_AstroUnifiedDashboardEA
// -----------------------------------------------------------------------------
// Why this exists:
// - Strategy Tester can be fragile with custom indicators under Shared Projects.
// - This EA draws everything itself with chart objects.
// - It does NOT use iCustom.
// - It does NOT send trades.
// - It reads the Python-generated CSV and renders:
//   1) compact text panel
//   2) pseudo-oscillator dot map in chart coordinates
//   3) diagnostics if the CSV cannot be loaded or matched.
//
// Runtime time contract:
// - Python CSV already contains broker_time.
// - Chart candle open time is matched directly against CSV broker_time.
// - No second GMT shift is applied for lookup.
// -----------------------------------------------------------------------------

enum DAL_AstroDashPreset
{
   ASTRO_DASH_COMPACT_JACKPOT = 0,
   ASTRO_DASH_RAW_AXES        = 1,
   ASTRO_DASH_MACRO           = 2,
   ASTRO_DASH_REGIME          = 3,
   ASTRO_DASH_MICRO_M1        = 4,
   ASTRO_DASH_M1_PATH         = 5,
   ASTRO_DASH_ALL_TEXT        = 6
};

input string              InpAstroCsvFile             = "astro_GMT3_M1_2026_to_now_mql.csv";
input double              InpBrokerGmtOffsetHours     = 0.0;
input bool                InpRequireExactBarTime      = true;
input int                 InpReloadCsvEverySeconds    = 0;      // 0 = load once. For live Python rolling CSV use 10..60.
input DAL_AstroDashPreset InpPreset                    = ASTRO_DASH_M1_PATH;

input bool                InpShowTextPanel            = true;
input bool                InpShowOscillator           = true;
input bool                InpUseTerminalComment       = false;
input int                 InpRefreshSeconds           = 1;

input int                 InpPanelX                   = 10;
input int                 InpPanelY                   = 18;
input int                 InpPanelFontSize            = 8;
input int                 InpPanelLineHeight          = 13;
input int                 InpPanelMaxLines            = 46;

input int                 InpOscX                     = 10;
input int                 InpOscY                     = 330;
input int                 InpOscWidth                 = 620;
input int                 InpOscHeight                = 185;
input int                 InpOscBars                  = 90;
input int                 InpOscDotSize               = 3;
input bool                InpOscShowLegend            = true;

input color               InpColorBackground          = clrBlack;
input color               InpColorText                = clrWhite;
input color               InpColorMuted               = clrDimGray;
input color               InpColorGood                = clrLime;
input color               InpColorRisk                = clrTomato;
input color               InpColorWarn                = clrOrange;
input color               InpColorInfo                = clrAqua;

DAL_AstroMapStore g_store;
bool     g_loaded = false;
datetime g_last_load_time = 0;
datetime g_last_render_time = 0;
string   g_prefix = "DAL_EXP0013_UNIFIED_ASTRO";

// -------------------------
// Object helpers
// -------------------------

void DAL_AD_DeleteByPrefix(const string prefix)
{
   long chart_id = ChartID();
   int total = ObjectsTotal(chart_id, -1, -1);
   for(int i = total - 1; i >= 0; i--)
   {
      string name = ObjectName(chart_id, i, -1, -1);
      if(StringFind(name, prefix) == 0)
         ObjectDelete(chart_id, name);
   }
}

void DAL_AD_Rect(const string name, const int x, const int y, const int w, const int h, const color bg, const color border = clrNONE)
{
   long chart_id = ChartID();
   if(ObjectFind(chart_id, name) < 0)
      ObjectCreate(chart_id, name, OBJ_RECTANGLE_LABEL, 0, 0, 0);

   ObjectSetInteger(chart_id, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(chart_id, name, OBJPROP_XSIZE, w);
   ObjectSetInteger(chart_id, name, OBJPROP_YSIZE, h);
   ObjectSetInteger(chart_id, name, OBJPROP_BGCOLOR, bg);
   ObjectSetInteger(chart_id, name, OBJPROP_BORDER_TYPE, BORDER_FLAT);
   ObjectSetInteger(chart_id, name, OBJPROP_COLOR, border);
   ObjectSetInteger(chart_id, name, OBJPROP_BACK, false);
   ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(chart_id, name, OBJPROP_HIDDEN, true);
}

void DAL_AD_Label(const string name, const string text, const int x, const int y, const color clr, const int font_size = 8)
{
   long chart_id = ChartID();
   if(ObjectFind(chart_id, name) < 0)
      ObjectCreate(chart_id, name, OBJ_LABEL, 0, 0, 0);

   ObjectSetInteger(chart_id, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetString(chart_id, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(chart_id, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(chart_id, name, OBJPROP_HIDDEN, true);
   ObjectSetString(chart_id, name, OBJPROP_TEXT, text);
}

void DAL_AD_Dot(const string name, const int x, const int y, const int size, const color clr)
{
   DAL_AD_Rect(name, x, y, size, size, clr, clr);
}

string DAL_AD_Double1(const double v)
{
   return DoubleToString(v, 1);
}

string DAL_AD_TimeText(const datetime t)
{
   if(t <= 0) return "n/a";
   return TimeToString(t, TIME_DATE | TIME_MINUTES);
}

string DAL_AD_Bucket(const double v)
{
   if(v < 20.0) return "very_low";
   if(v < 40.0) return "low";
   if(v < 60.0) return "mid";
   if(v < 80.0) return "high";
   return "very_high";
}

color DAL_AD_ValueColor(const string name, const double v)
{
   // For risk metrics, higher is bad.
   if(name == "Friction" || name == "Pressure" || name == "Transition" ||
      name == "PullbackRisk" || name == "ChopRisk" || name == "M1DirtyWindow" ||
      name == "MacroDrag" || name == "MacroPressure" || name == "MacroTransition" ||
      name == "OuterStation" || name == "MarsSatFriction" || name == "MercuryNoise" ||
      name == "MoonPressure" || name == "MoonDrag" || name == "MoonBoundary" ||
      name == "MicroNoise" || name == "SaturnResistance")
   {
      if(v >= 70.0) return InpColorRisk;
      if(v >= 45.0) return InpColorWarn;
      return InpColorGood;
   }

   // For constructive metrics, higher is good.
   if(v >= 70.0) return InpColorGood;
   if(v >= 45.0) return InpColorInfo;
   if(v >= 25.0) return InpColorWarn;
   return InpColorMuted;
}

// -------------------------
// CSV loading
// -------------------------

bool DAL_AD_LoadStore()
{
   g_last_load_time = TimeCurrent();

   g_loaded = DAL_AstroMapStore_LoadExcelCsv(
      g_store,
      InpAstroCsvFile,
      InpBrokerGmtOffsetHours,
      PeriodSeconds(_Period) / 60
   );

   if(!g_loaded)
   {
      Print("EXP0013 Unified Dashboard | CSV load failed | file=", InpAstroCsvFile);
      return false;
   }

   Print("EXP0013 Unified Dashboard | CSV loaded | rows=", g_store.row_count, " | source=", g_store.source_file);
   return true;
}

bool DAL_AD_ShouldReload()
{
   if(InpReloadCsvEverySeconds <= 0)
      return false;
   if(g_last_load_time <= 0)
      return true;
   return (TimeCurrent() - g_last_load_time) >= InpReloadCsvEverySeconds;
}

// -------------------------
// Metric extraction by preset
// -------------------------

int DAL_AD_PresetCount()
{
   if(InpPreset == ASTRO_DASH_COMPACT_JACKPOT) return 6;
   if(InpPreset == ASTRO_DASH_RAW_AXES)        return 7;
   if(InpPreset == ASTRO_DASH_MACRO)           return 8;
   if(InpPreset == ASTRO_DASH_REGIME)          return 8;
   if(InpPreset == ASTRO_DASH_MICRO_M1)        return 8;
   if(InpPreset == ASTRO_DASH_M1_PATH)         return 8;
   return 8;
}

string DAL_AD_PresetName()
{
   if(InpPreset == ASTRO_DASH_COMPACT_JACKPOT) return "COMPACT_JACKPOT";
   if(InpPreset == ASTRO_DASH_RAW_AXES)        return "RAW_AXES";
   if(InpPreset == ASTRO_DASH_MACRO)           return "MACRO_BACKGROUND";
   if(InpPreset == ASTRO_DASH_REGIME)          return "REGIME_ENGINE";
   if(InpPreset == ASTRO_DASH_MICRO_M1)        return "MOON_MICRO_M1";
   if(InpPreset == ASTRO_DASH_M1_PATH)         return "M1_PATH_QUALITY";
   return "ALL_TEXT";
}

bool DAL_AD_GetMetric(const DAL_AstroFractalMetrics &f, const int idx, string &name, double &value)
{
   name = "";
   value = 0.0;

   if(InpPreset == ASTRO_DASH_COMPACT_JACKPOT)
   {
      if(idx == 0) { name = "M1CleanWindow"; value = f.m1_clean_window; return true; }
      if(idx == 1) { name = "M1DirtyWindow"; value = f.m1_dirty_window; return true; }
      if(idx == 2) { name = "BreakoutFT"; value = f.breakout_followthrough; return true; }
      if(idx == 3) { name = "PullbackRisk"; value = f.pullback_risk; return true; }
      if(idx == 4) { name = "CleanImpulse"; value = f.clean_impulse; return true; }
      if(idx == 5) { name = "ChopRisk"; value = f.chop_risk; return true; }
      return false;
   }

   if(InpPreset == ASTRO_DASH_RAW_AXES)
   {
      if(idx == 0) { name = "Flow"; value = f.raw_flow; return true; }
      if(idx == 1) { name = "Impulse"; value = f.raw_impulse; return true; }
      if(idx == 2) { name = "Friction"; value = f.raw_friction; return true; }
      if(idx == 3) { name = "Pressure"; value = f.raw_pressure; return true; }
      if(idx == 4) { name = "Transition"; value = f.raw_transition; return true; }
      if(idx == 5) { name = "MoonTempo"; value = f.raw_moon_tempo; return true; }
      if(idx == 6) { name = "SaturnDrag"; value = f.raw_saturn_drag; return true; }
      return false;
   }

   if(InpPreset == ASTRO_DASH_MACRO)
   {
      if(idx == 0) { name = "MacroFlow"; value = f.macro_flow; return true; }
      if(idx == 1) { name = "MacroDrag"; value = f.macro_drag; return true; }
      if(idx == 2) { name = "MacroPressure"; value = f.macro_pressure; return true; }
      if(idx == 3) { name = "MacroTransition"; value = f.macro_transition; return true; }
      if(idx == 4) { name = "Expansion"; value = f.macro_expansion; return true; }
      if(idx == 5) { name = "Compression"; value = f.macro_compression; return true; }
      if(idx == 6) { name = "OuterStation"; value = f.outer_station_risk; return true; }
      if(idx == 7) { name = "StructuralBias"; value = f.structural_bias; return true; }
      return false;
   }

   if(InpPreset == ASTRO_DASH_REGIME)
   {
      if(idx == 0) { name = "MarsImpulse"; value = f.mars_impulse; return true; }
      if(idx == 1) { name = "MarsCleanImpulse"; value = f.mars_clean_impulse; return true; }
      if(idx == 2) { name = "MarsSatFriction"; value = f.mars_saturn_friction; return true; }
      if(idx == 3) { name = "MarsJupExpansion"; value = f.mars_jupiter_expansion; return true; }
      if(idx == 4) { name = "MercuryNoise"; value = f.mercury_noise; return true; }
      if(idx == 5) { name = "VenusMarsCoh"; value = f.venus_mars_cohesion; return true; }
      if(idx == 6) { name = "JupiterSupport"; value = f.jupiter_support; return true; }
      if(idx == 7) { name = "SaturnResistance"; value = f.saturn_resistance; return true; }
      return false;
   }

   if(InpPreset == ASTRO_DASH_MICRO_M1)
   {
      if(idx == 0) { name = "MoonTempo"; value = f.moon_tempo; return true; }
      if(idx == 1) { name = "MoonPressure"; value = f.moon_pressure; return true; }
      if(idx == 2) { name = "MoonFlow"; value = f.moon_flow; return true; }
      if(idx == 3) { name = "MoonDrag"; value = f.moon_drag; return true; }
      if(idx == 4) { name = "MoonBoundary"; value = f.moon_boundary; return true; }
      if(idx == 5) { name = "MoonOOB"; value = f.moon_oob_intensity; return true; }
      if(idx == 6) { name = "MicroNoise"; value = f.micro_noise; return true; }
      if(idx == 7) { name = "MicroClean"; value = f.micro_cleanliness; return true; }
      return false;
   }

   // Default M1 path-quality preset.
   if(idx == 0) { name = "CleanPath"; value = f.clean_path; return true; }
   if(idx == 1) { name = "CleanImpulse"; value = f.clean_impulse; return true; }
   if(idx == 2) { name = "SmoothCont"; value = f.smooth_continuation; return true; }
   if(idx == 3) { name = "BreakoutFT"; value = f.breakout_followthrough; return true; }
   if(idx == 4) { name = "PullbackRisk"; value = f.pullback_risk; return true; }
   if(idx == 5) { name = "ChopRisk"; value = f.chop_risk; return true; }
   if(idx == 6) { name = "M1CleanWindow"; value = f.m1_clean_window; return true; }
   if(idx == 7) { name = "M1DirtyWindow"; value = f.m1_dirty_window; return true; }
   return false;
}

bool DAL_AD_GetFractalForBarShift(const int shift, DAL_AstroFractalMetrics &f)
{
   DAL_AstroFM_Reset(f);
   datetime candle_time = iTime(_Symbol, _Period, shift);
   if(candle_time <= 0)
      return false;

   DAL_AstroMapRow row;
   if(!DAL_AstroMapStore_FindForCandleOpen(g_store, candle_time, row, InpRequireExactBarTime))
      return false;

   return DAL_AstroFM_Calc(row, f) && f.valid;
}

// -------------------------
// Rendering
// -------------------------

void DAL_AD_DrawTextPanel(const DAL_AstroFractalMetrics &f, const bool found)
{
   if(!InpShowTextPanel)
      return;

   int lines = InpPanelMaxLines;
   int panel_h = MathMax(120, lines * InpPanelLineHeight + 12);
   int panel_w = 640;
   DAL_AD_Rect(g_prefix + "_PANEL_BG", InpPanelX - 6, InpPanelY - 6, panel_w, panel_h, C'0,0,0', InpColorMuted);

   int y = InpPanelY;
   int n = 0;

   DAL_AD_Label(g_prefix + "_L_" + IntegerToString(n++), "EXP0013 ASTRO UNIFIED DASHBOARD EA  |  no-trade / no-iCustom / object-rendered", InpPanelX, y, InpColorInfo, InpPanelFontSize); y += InpPanelLineHeight;
   DAL_AD_Label(g_prefix + "_L_" + IntegerToString(n++), "Symbol=" + _Symbol + " TF=" + EnumToString(_Period) + " Preset=" + DAL_AD_PresetName(), InpPanelX, y, InpColorText, InpPanelFontSize); y += InpPanelLineHeight;

   if(!g_loaded)
   {
      DAL_AD_Label(g_prefix + "_L_" + IntegerToString(n++), "CSV STATUS: NOT LOADED", InpPanelX, y, InpColorRisk, InpPanelFontSize); y += InpPanelLineHeight;
      DAL_AD_Label(g_prefix + "_L_" + IntegerToString(n++), "Input file: " + InpAstroCsvFile, InpPanelX, y, InpColorWarn, InpPanelFontSize); y += InpPanelLineHeight;
      DAL_AD_Label(g_prefix + "_L_" + IntegerToString(n++), "Fix: put CSV in MQL5\\Files, MQL5\\Files\\astro, or Common\\Files.", InpPanelX, y, InpColorText, InpPanelFontSize); y += InpPanelLineHeight;
      return;
   }

   DAL_AD_Label(g_prefix + "_L_" + IntegerToString(n++), "CSV STATUS: LOADED rows=" + IntegerToString(g_store.row_count) + " source=" + g_store.source_file, InpPanelX, y, InpColorGood, InpPanelFontSize); y += InpPanelLineHeight;

   if(!found)
   {
      DAL_AD_Label(g_prefix + "_L_" + IntegerToString(n++), "ROW STATUS: NOT FOUND for chart candle open=" + DAL_AD_TimeText(iTime(_Symbol, _Period, 0)), InpPanelX, y, InpColorRisk, InpPanelFontSize); y += InpPanelLineHeight;
      DAL_AD_Label(g_prefix + "_L_" + IntegerToString(n++), "If this is live, generate/update a rolling CSV from Python or set RequireExact=false for diagnostics.", InpPanelX, y, InpColorWarn, InpPanelFontSize); y += InpPanelLineHeight;
      return;
   }

   DAL_AD_Label(g_prefix + "_L_" + IntegerToString(n++), "Broker=" + DAL_AD_TimeText(f.broker_time) + "  UTC=" + DAL_AD_TimeText(f.utc_time) + "  lookup=chart_open==csv_broker_time", InpPanelX, y, InpColorText, InpPanelFontSize); y += InpPanelLineHeight;

   int count = DAL_AD_PresetCount();
   for(int i = 0; i < count && n < InpPanelMaxLines - 6; i++)
   {
      string name; double value;
      if(!DAL_AD_GetMetric(f, i, name, value))
         continue;
      string line = StringFormat("%-18s %6.1f   %-9s", name, value, DAL_AD_Bucket(value));
      DAL_AD_Label(g_prefix + "_L_" + IntegerToString(n++), line, InpPanelX, y, DAL_AD_ValueColor(name, value), InpPanelFontSize);
      y += InpPanelLineHeight;
   }

   y += 3;
   DAL_AD_Label(g_prefix + "_L_" + IntegerToString(n++), f.thesis, InpPanelX, y, InpColorInfo, InpPanelFontSize); y += InpPanelLineHeight;
   DAL_AD_Label(g_prefix + "_L_" + IntegerToString(n++), "No causality claim. Validate with MAE_R / pullback_depth_R / path_efficiency.", InpPanelX, y, InpColorWarn, InpPanelFontSize);
}

void DAL_AD_DrawOscillator()
{
   if(!InpShowOscillator)
      return;

   int x = InpOscX;
   int y = InpOscY;
   int w = InpOscWidth;
   int h = InpOscHeight;

   DAL_AD_Rect(g_prefix + "_OSC_BG", x - 6, y - 18, w + 12, h + 28, C'0,0,0', InpColorMuted);
   DAL_AD_Label(g_prefix + "_OSC_TITLE", "ASTRO OSCILLATOR 0..100 | " + DAL_AD_PresetName(), x, y - 16, InpColorInfo, 8);

   // Horizontal levels.
   int inner_x = x + 70;
   int inner_y = y + 10;
   int inner_w = w - 82;
   int inner_h = h - 24;

   double levels[5] = {0.0, 25.0, 50.0, 75.0, 100.0};
   for(int li = 0; li < 5; li++)
   {
      int ly = inner_y + inner_h - (int)MathRound(levels[li] / 100.0 * inner_h);
      DAL_AD_Rect(g_prefix + "_LEV_" + IntegerToString(li), inner_x, ly, inner_w, 1, InpColorMuted, InpColorMuted);
      DAL_AD_Label(g_prefix + "_LEVT_" + IntegerToString(li), DoubleToString(levels[li], 0), x + 38, ly - 6, InpColorMuted, 7);
   }

   int count = DAL_AD_PresetCount();
   int bars = MathMax(10, MathMin(InpOscBars, 220));
   double step = (double)inner_w / (double)MathMax(1, bars - 1);

   // Legend.
   if(InpOscShowLegend)
   {
      int ly0 = inner_y;
      for(int s = 0; s < count; s++)
      {
         DAL_AstroFractalMetrics f0;
         DAL_AstroFM_Reset(f0);
         string nm = ""; double dummy = 0.0;
         if(DAL_AD_GetFractalForBarShift(0, f0))
            DAL_AD_GetMetric(f0, s, nm, dummy);
         else
         {
            // Get just the name from a zero struct.
            DAL_AD_GetMetric(f0, s, nm, dummy);
         }
         DAL_AD_Label(g_prefix + "_LEG_" + IntegerToString(s), nm, x + 2, ly0 + s * 13, DAL_AD_ValueColor(nm, 70.0), 7);
      }
   }

   for(int i = bars - 1; i >= 0; i--)
   {
      DAL_AstroFractalMetrics f;
      if(!DAL_AD_GetFractalForBarShift(i, f))
         continue;

      int px = inner_x + (int)MathRound((bars - 1 - i) * step);

      for(int s = 0; s < count; s++)
      {
         string name; double value;
         if(!DAL_AD_GetMetric(f, s, name, value))
            continue;

         value = MathMax(0.0, MathMin(100.0, value));
         int py = inner_y + inner_h - (int)MathRound(value / 100.0 * inner_h);
         color c = DAL_AD_ValueColor(name, value);
         DAL_AD_Dot(g_prefix + "_DOT_" + IntegerToString(s) + "_" + IntegerToString(i), px, py, InpOscDotSize, c);
      }
   }
}

void DAL_AD_Render()
{
   if(DAL_AD_ShouldReload())
      DAL_AD_LoadStore();

   // Full redraw prevents stale objects when preset changes.
   DAL_AD_DeleteByPrefix(g_prefix);

   DAL_AstroFractalMetrics f;
   bool found = false;
   if(g_loaded)
      found = DAL_AD_GetFractalForBarShift(0, f);

   if(InpShowTextPanel)
      DAL_AD_DrawTextPanel(f, found);

   if(InpShowOscillator && g_loaded)
      DAL_AD_DrawOscillator();

   if(InpUseTerminalComment)
   {
      if(!g_loaded)
         Comment("EXP0013 Astro Dashboard | CSV NOT LOADED | ", InpAstroCsvFile);
      else if(!found)
         Comment("EXP0013 Astro Dashboard | ROW NOT FOUND | candle=", DAL_AD_TimeText(iTime(_Symbol, _Period, 0)));
      else
         Comment("EXP0013 Astro Dashboard | ", DAL_AD_PresetName(), " | ", f.thesis);
   }

   ChartRedraw(ChartID());
}

int OnInit()
{
   g_prefix = "DAL_EXP0013_UNIFIED_ASTRO_" + IntegerToString((int)ChartID());
   EventSetTimer(MathMax(1, InpRefreshSeconds));
   DAL_AD_LoadStore();
   DAL_AD_Render();
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   DAL_AD_DeleteByPrefix(g_prefix);
   if(InpUseTerminalComment)
      Comment("");
}

void OnTick()
{
   datetime now_bar = iTime(_Symbol, _Period, 0);
   if(now_bar != g_last_render_time)
   {
      g_last_render_time = now_bar;
      DAL_AD_Render();
   }
}

void OnTimer()
{
   DAL_AD_Render();
}
