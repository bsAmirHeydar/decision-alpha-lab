#property strict
#property version   "1.00"
#property description "Decision Alpha Lab EXP0013 - Visual Tester host for the Astro Fractal Oscillator."
#property description "This EA does not trade. It only loads the oscillator into Visual Tester."

#property tester_indicator "Research\\EXP0013_AstroFractalOscillator.ex5"
#property tester_indicator "EXP0013_AstroFractalOscillator.ex5"
#property tester_file "astro_GMT3_M1_2026_to_now_mql.csv"
#property tester_file "astro\\astro_GMT3_M1_2026_to_now_mql.csv"

// Keep this enum in the same order as the indicator input enum.
enum DAL_AstroFractalOscPreset
{
   ASTRO_OSC_RAW_AXES = 0,
   ASTRO_OSC_MACRO_BACKGROUND = 1,
   ASTRO_OSC_REGIME_ENGINE = 2,
   ASTRO_OSC_MOON_MICRO = 3,
   ASTRO_OSC_M1_PATH_QUALITY = 4,
   ASTRO_OSC_COMPACT_JACKPOT = 5
};

input string                    InpIndicatorPath        = "Research\\EXP0013_AstroFractalOscillator";
input string                    InpAstroCsvFile         = "astro_GMT3_M1_2026_to_now_mql.csv";
input double                    InpBrokerGmtOffsetHours = 0.0;
input bool                      InpRequireExactBarTime  = true;
input int                       InpMaxBarsToProcess     = 10000;
input DAL_AstroFractalOscPreset InpPreset               = ASTRO_OSC_M1_PATH_QUALITY;
input bool                      InpShowDiagnosticsLine  = true;
input bool                      InpTryFallbackPaths     = true;
input bool                      InpAddIndicatorToChart  = true;

int    g_handle = INVALID_HANDLE;
string g_loaded_path = "";
string g_last_error_text = "";

string DAL_AstroHost_ErrorText(const int err)
{
   if(err == 0)    return "no error";
   if(err == 3)    return "path not found / folder was selected instead of a compiled file";
   if(err == 4802) return "indicator cannot be created: not compiled or wrong iCustom path";
   if(err == 4806) return "indicator handle invalid or custom indicator not ready";
   return "error=" + IntegerToString(err);
}

int DAL_AstroHost_CreateHandle(const string indicator_path)
{
   ResetLastError();
   int h = iCustom(
      _Symbol,
      _Period,
      indicator_path,
      InpAstroCsvFile,
      InpBrokerGmtOffsetHours,
      InpRequireExactBarTime,
      InpMaxBarsToProcess,
      InpPreset,
      InpShowDiagnosticsLine
   );

   int err = GetLastError();
   if(h == INVALID_HANDLE)
   {
      Print("EXP0013 Astro Host | iCustom failed | path=", indicator_path,
            " | ", DAL_AstroHost_ErrorText(err));
      g_last_error_text = "iCustom failed: " + indicator_path + " | " + DAL_AstroHost_ErrorText(err);
   }
   else
   {
      Print("EXP0013 Astro Host | indicator handle created | path=", indicator_path);
   }
   return h;
}

bool DAL_AstroHost_LoadIndicator()
{
   string paths[];
   ArrayResize(paths, 0);

   int n = 0;
   ArrayResize(paths, n + 1);
   paths[n++] = InpIndicatorPath;

   if(InpTryFallbackPaths)
   {
      string p1 = "Research\\EXP0013_AstroFractalOscillator";
      string p2 = "EXP0013_AstroFractalOscillator";
      string p3 = "Shared Projects\\decision-alpha-lab\\mql5\\Indicators\\Research\\EXP0013_AstroFractalOscillator";

      if(p1 != InpIndicatorPath)
      {
         ArrayResize(paths, n + 1);
         paths[n++] = p1;
      }
      if(p2 != InpIndicatorPath)
      {
         ArrayResize(paths, n + 1);
         paths[n++] = p2;
      }
      if(p3 != InpIndicatorPath)
      {
         ArrayResize(paths, n + 1);
         paths[n++] = p3;
      }
   }

   for(int i = 0; i < ArraySize(paths); i++)
   {
      int h = DAL_AstroHost_CreateHandle(paths[i]);
      if(h != INVALID_HANDLE)
      {
         g_handle = h;
         g_loaded_path = paths[i];
         return true;
      }
   }

   return false;
}

bool DAL_AstroHost_AddToChart()
{
   if(g_handle == INVALID_HANDLE)
      return false;

   // For a separate-window custom indicator, adding it to subwindow index equal
   // to ChartWindowsTotal usually creates a new subwindow. If the terminal build
   // rejects that, we print a clear diagnostic instead of failing silently.
   int target_window = ChartWindowsTotal(0);
   if(target_window < 1)
      target_window = 1;

   ResetLastError();
   bool ok = ChartIndicatorAdd(0, target_window, g_handle);
   if(!ok)
   {
      int err = GetLastError();
      Print("EXP0013 Astro Host | ChartIndicatorAdd failed | window=", target_window,
            " | ", DAL_AstroHost_ErrorText(err),
            " | You can still attach the compiled indicator manually to the Visual Tester chart.");
      g_last_error_text = "ChartIndicatorAdd failed | window=" + IntegerToString(target_window)
                        + " | " + DAL_AstroHost_ErrorText(err);
      return false;
   }

   ChartRedraw(0);
   Print("EXP0013 Astro Host | indicator added to chart | window=", target_window,
         " | path=", g_loaded_path);
   return true;
}

string DAL_AstroHost_StatusText()
{
   string s = "EXP0013 ASTRO FRACTAL OSCILLATOR HOST\n";
   s += "EA host: loaded - NO TRADING\n";
   s += "symbol=" + _Symbol + " tf=" + EnumToString(_Period) + "\n";
   s += "indicator_path=" + (g_loaded_path == "" ? InpIndicatorPath : g_loaded_path) + "\n";
   s += "csv=" + InpAstroCsvFile + "\n";
   s += "preset=" + IntegerToString((int)InpPreset) + "\n";

   if(g_handle == INVALID_HANDLE)
   {
      s += "STATUS: INDICATOR HANDLE FAILED\n";
      s += g_last_error_text + "\n";
      s += "Fix: compile the indicator, then select this EA under Experts, not the Indicators folder.\n";
   }
   else
   {
      s += "STATUS: INDICATOR HANDLE OK\n";
      s += "If the subwindow is not visible, attach the indicator manually to the visual chart.\n";
   }
   return s;
}

int OnInit()
{
   Print("EXP0013 Astro Host | init | This EA is visual-only and sends no orders.");

   bool ok = DAL_AstroHost_LoadIndicator();
   if(ok && InpAddIndicatorToChart)
      DAL_AstroHost_AddToChart();

   Comment(DAL_AstroHost_StatusText());
   return INIT_SUCCEEDED;
}

void OnTick()
{
   Comment(DAL_AstroHost_StatusText());
}

void OnDeinit(const int reason)
{
   Comment("");
   if(g_handle != INVALID_HANDLE)
   {
      IndicatorRelease(g_handle);
      g_handle = INVALID_HANDLE;
   }
   Print("EXP0013 Astro Host | deinit | reason=", reason);
}
