#property strict
#property version   "1.00"
#property description "EXP0013 Astro Path Cleanliness Metrics Demo"
#property description "Research-only visual tester panel. No trading. Reads candle-aligned astro CSV and displays derived path-cleanliness metrics."

#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroPathCleanlinessMetrics.mqh>

// -----------------------------------------------------------------------------
// EXP0013_AstroPathCleanlinessMetrics_Demo
// -----------------------------------------------------------------------------
// Purpose:
//   Observe the sky-state metrics candle by candle inside Visual Tester or live.
//   This EA does NOT trade. It only loads the Python-generated CSV mirror and
//   displays interpreted astrological path metrics on screen.
//
// Runtime data path:
//   Put CSV here:
//   <MetaTrader Data Folder>/MQL5/Files/astro/your_file.csv
//
// Time contract:
//   CSV broker_time must be the same time base as broker candles.
//   UTC is validated as: utc_time = broker_time - InpBrokerGmtOffsetHours.
// -----------------------------------------------------------------------------

input string          InpAstroCsvFile            = "astro\\astro_XAUUSD_M1_202401_mql.csv";
input double          InpBrokerGmtOffsetHours    = 2.0;
input ENUM_TIMEFRAMES InpReadTimeframe           = PERIOD_M1;
input bool            InpRequireExactBarTime     = true;
input bool            InpReadOnlyOnNewBar        = true;
input bool            InpValidateUtcOffset       = true;

input bool            InpShowRawBodies           = true;
input bool            InpShowFeatureKeys         = true;
input bool            InpUseObjectPanel          = true;
input bool            InpUseTerminalComment      = true;
input int             InpPanelX                  = 10;
input int             InpPanelY                  = 20;
input int             InpPanelFontSize           = 8;
input int             InpPanelLineHeight         = 14;
input color           InpPanelColor              = clrWhite;
input bool            InpPrintMetricsOnNewBar    = true;

DAL_AstroMapStore g_astro_store;
datetime g_last_bar_time = 0;

int OnInit()
{
   int tf_minutes = PeriodSeconds(InpReadTimeframe) / 60;
   if(tf_minutes <= 0)
      tf_minutes = 1;

   bool ok = DAL_AstroMapStore_LoadExcelCsv(
      g_astro_store,
      InpAstroCsvFile,
      InpBrokerGmtOffsetHours,
      tf_minutes
   );

   if(!ok)
   {
      string msg = "EXP0013 ASTRO PATH METRICS LOAD FAILED\n";
      msg += "Put the CSV under MQL5/Files/" + InpAstroCsvFile + "\n";
      msg += "Then re-run the visual tester/live chart.";
      Comment(msg);
      Print(msg);
      return INIT_FAILED;
   }

   Print("EXP0013 Astro Path Metrics initialized. rows=", g_astro_store.row_count,
         " file=", InpAstroCsvFile,
         " broker_gmt_offset=", DoubleToString(InpBrokerGmtOffsetHours, 2),
         " tf_minutes=", tf_minutes);

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   DAL_AstroPM_DeletePanel(0, "EXP0013_PATH");
   Comment("");
}

void OnTick()
{
   datetime bar_time = iTime(_Symbol, InpReadTimeframe, 0);
   if(bar_time <= 0)
      return;

   // The metrics are designed to be read candle by candle. If this is true,
   // the panel updates only when a new candle opens, so every displayed state is
   // aligned with a completed candle boundary in the tester/live chart.
   if(InpReadOnlyOnNewBar && bar_time == g_last_bar_time)
      return;
   g_last_bar_time = bar_time;

   DAL_AstroMapRow row;
   bool found = DAL_AstroMapStore_FindForCandleOpen(g_astro_store, bar_time, row, InpRequireExactBarTime);
   if(!found)
   {
      string missing = "ASTRO PATH METRICS - ROW NOT FOUND\n";
      missing += "CSV: " + InpAstroCsvFile + "\n";
      missing += "bar broker time: " + TimeToString(bar_time, TIME_DATE | TIME_MINUTES) + "\n";
      missing += "Require exact: " + (InpRequireExactBarTime ? "true" : "false") + "\n";
      missing += "Check timeframe, broker GMT offset, and CSV date range.";

      if(InpUseTerminalComment)
         Comment(missing);
      if(InpUseObjectPanel)
         DAL_AstroPM_DrawPanel(0, "EXP0013_PATH", missing, InpPanelX, InpPanelY, clrTomato, InpPanelFontSize, InpPanelLineHeight, true);
      return;
   }

   if(InpValidateUtcOffset && !DAL_AstroMapRow_ValidateUtcOffset(row, InpBrokerGmtOffsetHours, 2))
   {
      string bad = "ASTRO PATH METRICS - UTC OFFSET MISMATCH\n";
      bad += "row broker: " + TimeToString(row.broker_time, TIME_DATE | TIME_MINUTES) + "\n";
      bad += "row utc:    " + TimeToString(row.utc_time, TIME_DATE | TIME_MINUTES) + "\n";
      bad += "input offset hours: " + DoubleToString(InpBrokerGmtOffsetHours, 2) + "\n";
      bad += "Expected rule: utc = broker - offset.";

      if(InpUseTerminalComment)
         Comment(bad);
      if(InpUseObjectPanel)
         DAL_AstroPM_DrawPanel(0, "EXP0013_PATH", bad, InpPanelX, InpPanelY, clrTomato, InpPanelFontSize, InpPanelLineHeight, true);
      return;
   }

   DAL_AstroPathMetrics metrics;
   if(!DAL_AstroPathMetrics_Calc(row, metrics))
   {
      string calc_bad = "ASTRO PATH METRICS - CALC FAILED\n";
      calc_bad += "bar: " + TimeToString(bar_time, TIME_DATE | TIME_MINUTES) + "\n";
      calc_bad += "Required bodies/aspects are missing from the row.";

      if(InpUseTerminalComment)
         Comment(calc_bad);
      if(InpUseObjectPanel)
         DAL_AstroPM_DrawPanel(0, "EXP0013_PATH", calc_bad, InpPanelX, InpPanelY, clrTomato, InpPanelFontSize, InpPanelLineHeight, true);
      return;
   }

   string panel = DAL_AstroPM_ToScreenText(row, metrics, InpShowRawBodies, InpShowFeatureKeys);

   if(InpUseTerminalComment)
      Comment(panel);

   if(InpUseObjectPanel)
      DAL_AstroPM_DrawPanel(0, "EXP0013_PATH", panel, InpPanelX, InpPanelY, InpPanelColor, InpPanelFontSize, InpPanelLineHeight, true);

   if(InpPrintMetricsOnNewBar)
   {
      Print("EXP0013_ASTRO_PATH bar=", TimeToString(bar_time, TIME_DATE | TIME_MINUTES),
            " clean=", DoubleToString(metrics.clean_path_score, 1),
            " flow=", DoubleToString(metrics.flow_score, 1),
            " impulse=", DoubleToString(metrics.impulse_score, 1),
            " friction=", DoubleToString(metrics.friction_score, 1),
            " pressure=", DoubleToString(metrics.pressure_score, 1),
            " transition=", DoubleToString(metrics.transition_score, 1),
            " pbRisk=", DoubleToString(metrics.pullback_risk_score, 1),
            " chopRisk=", DoubleToString(metrics.chop_risk_score, 1),
            " regime=", metrics.astro_path_regime,
            " key=", metrics.astro_path_key);
   }
}
