#property strict
#property description "Decision Alpha Lab - EXP0013 Astro Unified Dashboard EA"
#property description "Research-only visual dashboard. No orders. No iCustom. No indicator loading."
#property tester_file "astro_GMT3_M1_2026_to_now_mql.csv"
#property tester_file "astro\\astro_GMT3_M1_2026_to_now_mql.csv"
#property tester_file "astro_live_mql.csv"

#include <Research/DAL_AstroMapTypes.mqh>
#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroPathCleanlinessMetrics.mqh>
#include <Research/DAL_AstroFractalPathMetrics.mqh>

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

enum DAL_AstroDashboardView
{
   ASTRO_VIEW_SINGLE_PRESET = 0,
   ASTRO_VIEW_COCKPIT      = 1,
   ASTRO_VIEW_MICRO_FOCUS  = 2
};

input string              InpAstroCsvFile             = "astro_live_mql.csv";
input double              InpBrokerGmtOffsetHours     = 0.0;
input bool                InpRequireExactBarTime      = true;
input int                 InpReloadCsvEverySeconds    = 10;
input DAL_AstroDashPreset InpPreset                   = ASTRO_DASH_M1_PATH;
input DAL_AstroDashboardView InpViewMode               = ASTRO_VIEW_COCKPIT;

input bool                InpShowTextPanel            = true;
input bool                InpShowOscillator           = true;
input bool                InpUseTerminalComment       = false;
input int                 InpRefreshSeconds           = 1;

input int                 InpPanelX                   = 10;
input int                 InpPanelY                   = 18;
input int                 InpPanelWidth               = 760;
input int                 InpPanelFontSize            = 10;
input int                 InpPanelLineHeight          = 16;
input int                 InpPanelMaxLines            = 26;

input int                 InpOscX                     = 10;
input int                 InpOscY                     = 420;
input int                 InpOscWidth                 = 720;
input int                 InpOscRowHeight             = 20;
input int                 InpOscHistoryBars           = 90;
input int                 InpOscPointSize             = 2;
input bool                InpOscShowCurrentBar        = true;

input int                 InpCardWidth                = 355;
input int                 InpCardGap                  = 12;
input int                 InpCardRowHeight            = 17;
input bool                InpShowTimeline             = true;

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
string   g_prefix = "DAL_EXP0013_UNIFIED_ASTRO";
int      g_prev_text_count = 0;
int      g_prev_osc_count = 0;
int      g_prev_card_count = 0;

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

void DAL_AD_Rect(const string name, const int x, const int y, const int w, const int h, const color bg, const color border)
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
   ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, false);
   ObjectSetInteger(chart_id, name, OBJPROP_HIDDEN, true);
   ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, 0);
}

void DAL_AD_Label(const string name, const string text, const int x, const int y, const color clr, const int font_size, const string font = "Consolas")
{
   long chart_id = ChartID();
   if(ObjectFind(chart_id, name) < 0)
      ObjectCreate(chart_id, name, OBJ_LABEL, 0, 0, 0);

   ObjectSetInteger(chart_id, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetString(chart_id, name, OBJPROP_FONT, font);
   ObjectSetInteger(chart_id, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, false);
   ObjectSetInteger(chart_id, name, OBJPROP_HIDDEN, true);
   ObjectSetString(chart_id, name, OBJPROP_TEXT, text);
}

void DAL_AD_DeleteRange(const string stem, const int from_idx, const int to_idx)
{
   long chart_id = ChartID();
   for(int i = from_idx; i < to_idx; i++)
   {
      string n = stem + IntegerToString(i);
      if(ObjectFind(chart_id, n) >= 0)
         ObjectDelete(chart_id, n);
   }
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

string DAL_AD_Shorten(const string s, const int max_len)
{
   int len = StringLen(s);
   if(len <= max_len || max_len <= 6)
      return s;
   int keep = (max_len - 3) / 2;
   return StringSubstr(s, 0, keep) + "..." + StringSubstr(s, len - keep);
}

string DAL_AD_TrimText(const string s, const int max_len)
{
   if(StringLen(s) <= max_len) return s;
   return StringSubstr(s, 0, MathMax(0, max_len - 3)) + "...";
}

color DAL_AD_ValueColor(const string name, const double v)
{
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

   if(v >= 70.0) return InpColorGood;
   if(v >= 45.0) return InpColorInfo;
   if(v >= 25.0) return InpColorWarn;
   return InpColorMuted;
}

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
   name = ""; value = 0.0;
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


string DAL_AD_ViewName()
{
   if(InpViewMode == ASTRO_VIEW_SINGLE_PRESET) return "SINGLE_PRESET";
   if(InpViewMode == ASTRO_VIEW_COCKPIT)      return "COCKPIT";
   if(InpViewMode == ASTRO_VIEW_MICRO_FOCUS)  return "MICRO_FOCUS";
   return "VIEW";
}

datetime DAL_AD_CsvFirstTime()
{
   if(!g_loaded || g_store.row_count <= 0) return 0;
   return g_store.rows[0].broker_time;
}

datetime DAL_AD_CsvLastTime()
{
   if(!g_loaded || g_store.row_count <= 0) return 0;
   return g_store.rows[g_store.row_count - 1].broker_time;
}

bool DAL_AD_IsCsvStaleForChart()
{
   datetime last = DAL_AD_CsvLastTime();
   datetime chart_t = iTime(_Symbol, _Period, 0);
   if(last <= 0 || chart_t <= 0) return false;
   return chart_t > last;
}

string DAL_AD_PathVerdict(const DAL_AstroFractalMetrics &f)
{
   if(f.m1_clean_window >= 65.0 && f.pullback_risk <= 35.0 && f.chop_risk <= 40.0)
      return "CLEAN_WINDOW";
   if(f.m1_dirty_window >= 60.0 || f.chop_risk >= 65.0 || f.pullback_risk >= 65.0)
      return "DIRTY_WARNING";
   if(f.breakout_followthrough >= 65.0 && f.clean_impulse >= 55.0)
      return "BREAKOUT_SUPPORT";
   if(f.smooth_continuation >= 60.0 && f.pullback_risk <= 40.0)
      return "SMOOTH_CONT_SUPPORT";
   return "MIXED_NEUTRAL";
}

color DAL_AD_VerdictColor(const string verdict)
{
   if(verdict == "CLEAN_WINDOW" || verdict == "BREAKOUT_SUPPORT" || verdict == "SMOOTH_CONT_SUPPORT")
      return InpColorGood;
   if(verdict == "DIRTY_WARNING")
      return InpColorRisk;
   return InpColorInfo;
}

int DAL_AD_LayerCount(const int layer)
{
   return 6;
}

string DAL_AD_LayerTitle(const int layer)
{
   if(layer == 0) return "PATH QUALITY";
   if(layer == 1) return "MICRO M1";
   if(layer == 2) return "REGIME ENGINE";
   if(layer == 3) return "MACRO BACKGROUND";
   if(layer == 4) return "RAW AXES";
   return "LAYER";
}

bool DAL_AD_GetLayerMetric(const DAL_AstroFractalMetrics &f, const int layer, const int idx, string &name, double &value)
{
   name = "";
   value = 0.0;

   if(layer == 0)
   {
      if(idx == 0) { name = "CleanPath"; value = f.clean_path; return true; }
      if(idx == 1) { name = "CleanImpulse"; value = f.clean_impulse; return true; }
      if(idx == 2) { name = "BreakoutFT"; value = f.breakout_followthrough; return true; }
      if(idx == 3) { name = "PullbackRisk"; value = f.pullback_risk; return true; }
      if(idx == 4) { name = "ChopRisk"; value = f.chop_risk; return true; }
      if(idx == 5) { name = "M1CleanWindow"; value = f.m1_clean_window; return true; }
      return false;
   }

   if(layer == 1)
   {
      if(idx == 0) { name = "MoonTempo"; value = f.moon_tempo; return true; }
      if(idx == 1) { name = "MoonPressure"; value = f.moon_pressure; return true; }
      if(idx == 2) { name = "MoonFlow"; value = f.moon_flow; return true; }
      if(idx == 3) { name = "MoonDrag"; value = f.moon_drag; return true; }
      if(idx == 4) { name = "MicroNoise"; value = f.micro_noise; return true; }
      if(idx == 5) { name = "MicroClean"; value = f.micro_cleanliness; return true; }
      return false;
   }

   if(layer == 2)
   {
      if(idx == 0) { name = "MarsImpulse"; value = f.mars_impulse; return true; }
      if(idx == 1) { name = "MarsCleanImpulse"; value = f.mars_clean_impulse; return true; }
      if(idx == 2) { name = "MarsSatFriction"; value = f.mars_saturn_friction; return true; }
      if(idx == 3) { name = "MercuryNoise"; value = f.mercury_noise; return true; }
      if(idx == 4) { name = "JupiterSupport"; value = f.jupiter_support; return true; }
      if(idx == 5) { name = "SaturnResistance"; value = f.saturn_resistance; return true; }
      return false;
   }

   if(layer == 3)
   {
      if(idx == 0) { name = "MacroFlow"; value = f.macro_flow; return true; }
      if(idx == 1) { name = "MacroDrag"; value = f.macro_drag; return true; }
      if(idx == 2) { name = "MacroPressure"; value = f.macro_pressure; return true; }
      if(idx == 3) { name = "Expansion"; value = f.macro_expansion; return true; }
      if(idx == 4) { name = "Compression"; value = f.macro_compression; return true; }
      if(idx == 5) { name = "OuterStation"; value = f.outer_station_risk; return true; }
      return false;
   }

   if(layer == 4)
   {
      if(idx == 0) { name = "Flow"; value = f.raw_flow; return true; }
      if(idx == 1) { name = "Impulse"; value = f.raw_impulse; return true; }
      if(idx == 2) { name = "Friction"; value = f.raw_friction; return true; }
      if(idx == 3) { name = "Pressure"; value = f.raw_pressure; return true; }
      if(idx == 4) { name = "Transition"; value = f.raw_transition; return true; }
      if(idx == 5) { name = "SaturnDrag"; value = f.raw_saturn_drag; return true; }
      return false;
   }

   return false;
}

void DAL_AD_DrawMetricBar(const string stem, const string name, const double value, const int x, const int y, const int w, const int h)
{
   int label_w = 126;
   int value_w = 48;
   int bar_x = x + label_w;
   int bar_w = w - label_w - value_w - 8;
   if(bar_w < 40) bar_w = 40;

   color c = DAL_AD_ValueColor(name, value);
   DAL_AD_Label(stem + "_N", name, x, y, InpColorText, 8);
   DAL_AD_Label(stem + "_V", DoubleToString(value, 1), x + w - value_w, y, c, 8);
   DAL_AD_Rect(stem + "_BG", bar_x, y + 4, bar_w, MathMax(5, h - 8), C'18,18,18', InpColorMuted);
   int fill_w = (int)MathRound((MathMax(0.0, MathMin(100.0, value)) / 100.0) * bar_w);
   DAL_AD_Rect(stem + "_F", bar_x, y + 4, fill_w, MathMax(5, h - 8), c, c);
   DAL_AD_Rect(stem + "_MID", bar_x + bar_w / 2, y + 3, 1, MathMax(7, h - 6), InpColorMuted, InpColorMuted);
}

void DAL_AD_DrawLayerCard(const DAL_AstroFractalMetrics &f, const int layer, const int x, const int y, const int w)
{
   int rows = DAL_AD_LayerCount(layer);
   int h = 26 + rows * InpCardRowHeight + 10;
   string stem = g_prefix + "_CARD_" + IntegerToString(layer);
   DAL_AD_Rect(stem + "_BG", x, y, w, h, InpColorBackground, InpColorMuted);
   DAL_AD_Label(stem + "_TITLE", DAL_AD_LayerTitle(layer), x + 8, y + 6, InpColorInfo, 9);

   for(int i = 0; i < rows; i++)
   {
      string name; double value;
      if(!DAL_AD_GetLayerMetric(f, layer, i, name, value))
         continue;
      DAL_AD_DrawMetricBar(stem + "_R_" + IntegerToString(i), name, value, x + 8, y + 26 + i * InpCardRowHeight, w - 16, InpCardRowHeight);
   }
}

void DAL_AD_DrawHeaderCard(const DAL_AstroFractalMetrics &f, const bool found)
{
   int x = InpPanelX;
   int y = InpPanelY;
   int w = MathMax(520, InpPanelWidth);
   int h = 112;
   DAL_AD_Rect(g_prefix + "_HEAD_BG", x - 8, y - 8, w, h, InpColorBackground, InpColorMuted);

   DAL_AD_Label(g_prefix + "_HEAD_0", "EXP0013 ASTRO COCKPIT EA  |  no-trade / no-iCustom / object-rendered", x, y, InpColorInfo, InpPanelFontSize);
   DAL_AD_Label(g_prefix + "_HEAD_1", "Symbol=" + _Symbol + "  TF=" + EnumToString(_Period) + "  View=" + DAL_AD_ViewName() + "  ReloadSec=" + IntegerToString(InpReloadCsvEverySeconds), x, y + InpPanelLineHeight, InpColorText, InpPanelFontSize);

   string csv_line;
   color csv_color = InpColorGood;
   if(!g_loaded)
   {
      csv_line = "CSV: NOT LOADED  input=" + DAL_AD_Shorten(InpAstroCsvFile, 54);
      csv_color = InpColorRisk;
   }
   else
   {
      csv_line = "CSV: LOADED rows=" + IntegerToString(g_store.row_count) + "  window=" + DAL_AD_TimeText(DAL_AD_CsvFirstTime()) + " -> " + DAL_AD_TimeText(DAL_AD_CsvLastTime());
      if(DAL_AD_IsCsvStaleForChart()) csv_color = InpColorRisk;
   }
   DAL_AD_Label(g_prefix + "_HEAD_2", csv_line, x, y + 2 * InpPanelLineHeight, csv_color, InpPanelFontSize);

   if(!g_loaded)
   {
      DAL_AD_Label(g_prefix + "_HEAD_3", "Fix: put CSV in MQL5\\Files, MQL5\\Files\\astro, or Common\\Files. Live: run Python bridge.", x, y + 3 * InpPanelLineHeight, InpColorWarn, InpPanelFontSize);
      return;
   }
   if(!found)
   {
      DAL_AD_Label(g_prefix + "_HEAD_3", "ROW: NOT FOUND for chart candle " + DAL_AD_TimeText(iTime(_Symbol, _Period, 0)) + "  | extend live CSV or disable exact only for diagnostics", x, y + 3 * InpPanelLineHeight, InpColorRisk, InpPanelFontSize);
      return;
   }

   string verdict = DAL_AD_PathVerdict(f);
   DAL_AD_Label(g_prefix + "_HEAD_3", "Broker=" + DAL_AD_TimeText(f.broker_time) + "  UTC=" + DAL_AD_TimeText(f.utc_time) + "  Verdict=" + verdict, x, y + 3 * InpPanelLineHeight, DAL_AD_VerdictColor(verdict), InpPanelFontSize);
   DAL_AD_Label(g_prefix + "_HEAD_4", DAL_AD_TrimText(f.thesis, 86), x, y + 4 * InpPanelLineHeight, InpColorInfo, InpPanelFontSize);
   DAL_AD_Label(g_prefix + "_HEAD_5", "Research rule: market gives direction; astro gives path-quality context. Validate with MAE_R / pullback_depth_R.", x, y + 5 * InpPanelLineHeight, InpColorWarn, InpPanelFontSize);
}

void DAL_AD_DrawCockpit(const DAL_AstroFractalMetrics &f, const bool found)
{
   if(!InpShowTextPanel && !InpShowOscillator)
      return;

   if(InpShowTextPanel)
      DAL_AD_DrawHeaderCard(f, found);

   if(!InpShowOscillator || !g_loaded || !found)
      return;

   int x0 = InpPanelX;
   int y0 = InpPanelY + 120;
   int w = InpCardWidth;
   int gap = InpCardGap;

   if(InpViewMode == ASTRO_VIEW_MICRO_FOCUS)
   {
      DAL_AD_DrawLayerCard(f, 1, x0, y0, w);
      DAL_AD_DrawLayerCard(f, 0, x0 + w + gap, y0, w);
      DAL_AD_DrawLayerCard(f, 2, x0, y0 + 142, w);
      DAL_AD_DrawLayerCard(f, 4, x0 + w + gap, y0 + 142, w);
      return;
   }

   DAL_AD_DrawLayerCard(f, 0, x0, y0, w);
   DAL_AD_DrawLayerCard(f, 1, x0 + w + gap, y0, w);
   DAL_AD_DrawLayerCard(f, 2, x0, y0 + 142, w);
   DAL_AD_DrawLayerCard(f, 3, x0 + w + gap, y0 + 142, w);
}

void DAL_AD_DrawTextPanel(const DAL_AstroFractalMetrics &f, const bool found)
{
   if(!InpShowTextPanel)
      return;

   int count = DAL_AD_PresetCount();
   int lines = 6 + count;
   lines = MathMin(lines, InpPanelMaxLines);
   int panel_h = MathMax(120, lines * InpPanelLineHeight + 16);
   DAL_AD_Rect(g_prefix + "_TXT_BG", InpPanelX - 8, InpPanelY - 8, InpPanelWidth, panel_h, InpColorBackground, InpColorMuted);

   int y = InpPanelY;
   int n = 0;
   DAL_AD_Label(g_prefix + "_TXT_" + IntegerToString(n++), "EXP0013 ASTRO DASHBOARD  |  " + DAL_AD_PresetName(), InpPanelX, y, InpColorInfo, InpPanelFontSize); y += InpPanelLineHeight;
   DAL_AD_Label(g_prefix + "_TXT_" + IntegerToString(n++), "Symbol=" + _Symbol + "   TF=" + EnumToString(_Period) + "   ReloadSec=" + IntegerToString(InpReloadCsvEverySeconds), InpPanelX, y, InpColorText, InpPanelFontSize); y += InpPanelLineHeight;

   string load_line = g_loaded ? ("CSV: LOADED  rows=" + IntegerToString(g_store.row_count) + "  src=" + DAL_AD_Shorten(g_store.source_file, 48))
                               : ("CSV: NOT LOADED  input=" + DAL_AD_Shorten(InpAstroCsvFile, 48));
   DAL_AD_Label(g_prefix + "_TXT_" + IntegerToString(n++), load_line, InpPanelX, y, g_loaded ? InpColorGood : InpColorRisk, InpPanelFontSize); y += InpPanelLineHeight;

   if(!g_loaded)
   {
      DAL_AD_Label(g_prefix + "_TXT_" + IntegerToString(n++), "Put CSV in MQL5\\Files, MQL5\\Files\\astro, or Common\\Files.", InpPanelX, y, InpColorWarn, InpPanelFontSize); y += InpPanelLineHeight;
      DAL_AD_Label(g_prefix + "_TXT_" + IntegerToString(n++), "For live bridge, use astro_live_mql.csv and ReloadSec=10..60.", InpPanelX, y, InpColorText, InpPanelFontSize); y += InpPanelLineHeight;
      if(g_prev_text_count > n) DAL_AD_DeleteRange(g_prefix + "_TXT_", n, g_prev_text_count);
      g_prev_text_count = n;
      return;
   }

   if(!found)
   {
      DAL_AD_Label(g_prefix + "_TXT_" + IntegerToString(n++), "ROW: NOT FOUND for chart candle " + DAL_AD_TimeText(iTime(_Symbol, _Period, 0)), InpPanelX, y, InpColorRisk, InpPanelFontSize); y += InpPanelLineHeight;
      DAL_AD_Label(g_prefix + "_TXT_" + IntegerToString(n++), "If live, extend Python rolling window or set exact=false only for diagnostics.", InpPanelX, y, InpColorWarn, InpPanelFontSize); y += InpPanelLineHeight;
      if(g_prev_text_count > n) DAL_AD_DeleteRange(g_prefix + "_TXT_", n, g_prev_text_count);
      g_prev_text_count = n;
      return;
   }

   DAL_AD_Label(g_prefix + "_TXT_" + IntegerToString(n++), "Broker=" + DAL_AD_TimeText(f.broker_time) + "   UTC=" + DAL_AD_TimeText(f.utc_time) + "   lookup=chart_open==csv_broker_time", InpPanelX, y, InpColorText, InpPanelFontSize); y += InpPanelLineHeight;

   for(int i = 0; i < count && n < InpPanelMaxLines - 2; i++)
   {
      string name; double value;
      if(!DAL_AD_GetMetric(f, i, name, value))
         continue;
      string line = name + "  " + DoubleToString(value, 1) + "  " + DAL_AD_Bucket(value);
      DAL_AD_Label(g_prefix + "_TXT_" + IntegerToString(n++), line, InpPanelX, y, DAL_AD_ValueColor(name, value), InpPanelFontSize); y += InpPanelLineHeight;
   }

   DAL_AD_Label(g_prefix + "_TXT_" + IntegerToString(n++), DAL_AD_TrimText(f.thesis, 74), InpPanelX, y, InpColorInfo, InpPanelFontSize); y += InpPanelLineHeight;
   DAL_AD_Label(g_prefix + "_TXT_" + IntegerToString(n++), "Validate with MAE_R / pullback_depth_R / path_efficiency.", InpPanelX, y, InpColorWarn, InpPanelFontSize); y += InpPanelLineHeight;

   if(g_prev_text_count > n)
      DAL_AD_DeleteRange(g_prefix + "_TXT_", n, g_prev_text_count);
   g_prev_text_count = n;
}

void DAL_AD_DrawOscillator()
{
   if(!InpShowOscillator)
      return;

   int count = DAL_AD_PresetCount();
   int row_h = MathMax(16, InpOscRowHeight);
   int title_h = 20;
   int pad = 8;
   int legend_w = 160;
   int value_w = 48;
   int hist_w = InpOscWidth - legend_w - value_w - 3 * pad;
   int total_h = title_h + pad + count * row_h + pad;

   DAL_AD_Rect(g_prefix + "_OSC_BG", InpOscX - 8, InpOscY - 8, InpOscWidth, total_h, InpColorBackground, InpColorMuted);
   DAL_AD_Label(g_prefix + "_OSC_TITLE", "ASTRO OSCILLATOR 0..100  |  " + DAL_AD_PresetName(), InpOscX, InpOscY, InpColorInfo, 10);

   int base_y = InpOscY + title_h;
   int hist_x0 = InpOscX + legend_w;
   int bars = MathMax(10, MathMin(InpOscHistoryBars, 220));
   double step = (double)hist_w / (double)MathMax(1, bars - 1);

   int obj_idx = 0;
   for(int s = 0; s < count; s++)
   {
      DAL_AstroFractalMetrics f0;
      DAL_AstroFM_Reset(f0);
      string name = ""; double cur_value = 0.0;
      bool ok0 = DAL_AD_GetFractalForBarShift(0, f0);
      DAL_AD_GetMetric(f0, s, name, cur_value);
      int row_y = base_y + s * row_h;
      int center_y = row_y + row_h / 2;
      color row_clr = DAL_AD_ValueColor(name, cur_value);

      DAL_AD_Label(g_prefix + "_OSC_LBL_" + IntegerToString(s), name, InpOscX, row_y + 1, InpColorText, 8);
      DAL_AD_Label(g_prefix + "_OSC_VAL_" + IntegerToString(s), ok0 ? DoubleToString(cur_value, 1) : "n/a", InpOscX + legend_w - 46, row_y + 1, row_clr, 8);
      DAL_AD_Rect(g_prefix + "_OSC_LINE_" + IntegerToString(s), hist_x0, center_y, hist_w, 1, InpColorMuted, InpColorMuted);

      // current bar mini bar
      if(InpOscShowCurrentBar && ok0)
      {
         int bar_w = 36;
         int bar_h = MathMax(6, row_h - 8);
         int bar_x = InpOscX + legend_w - value_w - 4;
         int bar_y = row_y + 4;
         DAL_AD_Rect(g_prefix + "_OSC_BAR_BG_" + IntegerToString(s), bar_x, bar_y, bar_w, bar_h, C'20,20,20', InpColorMuted);
         int fill_w = (int)MathRound((MathMax(0.0, MathMin(100.0, cur_value)) / 100.0) * bar_w);
         DAL_AD_Rect(g_prefix + "_OSC_BAR_FILL_" + IntegerToString(s), bar_x, bar_y, fill_w, bar_h, row_clr, row_clr);
      }

      for(int i = bars - 1; i >= 0; i--)
      {
         DAL_AstroFractalMetrics f;
         if(!DAL_AD_GetFractalForBarShift(i, f))
            continue;
         string nm; double value;
         if(!DAL_AD_GetMetric(f, s, nm, value))
            continue;

         value = MathMax(0.0, MathMin(100.0, value));
         int px = hist_x0 + (int)MathRound((bars - 1 - i) * step);
         int py = row_y + row_h - 4 - (int)MathRound((value / 100.0) * (row_h - 8));
         DAL_AD_Rect(g_prefix + "_OSC_PT_" + IntegerToString(obj_idx++), px, py, InpOscPointSize, InpOscPointSize, DAL_AD_ValueColor(name, value), DAL_AD_ValueColor(name, value));
      }
   }

   if(g_prev_osc_count > obj_idx)
      DAL_AD_DeleteRange(g_prefix + "_OSC_PT_", obj_idx, g_prev_osc_count);
   g_prev_osc_count = obj_idx;
}

void DAL_AD_Render()
{
   bool reloaded = false;
   if(DAL_AD_ShouldReload())
   {
      reloaded = true;
      DAL_AD_LoadStore();
   }

   DAL_AstroFractalMetrics f;
   bool found = false;
   if(g_loaded)
      found = DAL_AD_GetFractalForBarShift(0, f);

   if(InpViewMode == ASTRO_VIEW_SINGLE_PRESET)
   {
      if(InpShowTextPanel)
         DAL_AD_DrawTextPanel(f, found);
      if(InpShowOscillator)
         DAL_AD_DrawOscillator();
   }
   else
   {
      DAL_AD_DrawCockpit(f, found);
   }

   if(InpUseTerminalComment)
   {
      if(!g_loaded)
         Comment("EXP0013 Astro Dashboard | CSV NOT LOADED | ", InpAstroCsvFile);
      else if(!found)
         Comment("EXP0013 Astro Dashboard | ROW NOT FOUND | candle=", DAL_AD_TimeText(iTime(_Symbol, _Period, 0)));
      else
         Comment("EXP0013 Astro Dashboard | ", DAL_AD_PresetName(), " | ", f.thesis, reloaded ? " | reloaded" : "");
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
   // Keep rendering timer-driven to avoid object flicker and redundant tick-by-tick redraw.
}

void OnTimer()
{
   DAL_AD_Render();
}
