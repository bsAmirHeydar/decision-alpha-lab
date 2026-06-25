#property strict
#property version   "1.00"
#property description "EXP0013 Astro Excel/CSV Candle Reader Demo"
#property description "Loads Python-generated candle-aligned astro CSV and displays the sky map per candle."
#property tester_file "astro_GMT3_M1_2026_to_now_mql.csv"
#property tester_file "astro\\astro_GMT3_M1_2026_to_now_mql.csv"

#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroDerivedFeatures.mqh>

input string          InpAstroCsvFile            = "astro_GMT3_M1_2026_to_now_mql.csv";
input double          InpBrokerGmtOffsetHours    = 0.0; // optional UTC validation only; lookup never shifts time
input ENUM_TIMEFRAMES InpReadTimeframe           = PERIOD_M1;
input bool            InpRequireExactBarTime     = true;
input bool            InpReadOnlyOnNewBar        = true;
input bool            InpValidateUtcOffset       = false;
input bool            InpShowDerivedFeatureKey   = true;
input bool            InpUseObjectPanel          = true;
input bool            InpUseTerminalComment      = false;
input bool            InpClearChartComment       = true;
input int             InpPanelX                  = 10;
input int             InpPanelY                  = 90;

DAL_AstroMapStore g_astro_store;
datetime g_last_bar_time = 0;

int OnInit()
{
   bool ok = DAL_AstroMapStore_LoadExcelCsv(
      g_astro_store,
      InpAstroCsvFile,
      InpBrokerGmtOffsetHours,
      PeriodSeconds(InpReadTimeframe) / 60
   );

   if(!ok)
   {
      string msg = DAL_AstroMapStore_LoadDiagnosticText(g_astro_store);
      msg += "\nEA STATUS: stayed loaded intentionally so the diagnostic is visible on screen.";
      Print(msg);
      if(InpUseTerminalComment)
         Comment(msg);
      else if(InpClearChartComment)
         Comment("");
      if(InpUseObjectPanel)
         DAL_AstroMap_DrawStatus(0, "EXP0013", msg, InpPanelX, InpPanelY, clrTomato);
      return INIT_SUCCEEDED;
   }

   Print("EXP0013 Astro reader initialized. rows=", g_astro_store.row_count,
         " file=", InpAstroCsvFile,
         " optional_utc_validation_offset=", DoubleToString(InpBrokerGmtOffsetHours, 2));
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   DAL_AstroDiag_DeletePanel(0, "EXP0013");
   Comment("");
}

void OnTick()
{
   datetime bar_time = iTime(_Symbol, InpReadTimeframe, 0);
   if(bar_time <= 0)
      return;

   if(InpReadOnlyOnNewBar && bar_time == g_last_bar_time)
      return;
   g_last_bar_time = bar_time;

   DAL_AstroMapRow row;
   bool found = DAL_AstroMapStore_FindForCandleOpen(g_astro_store, bar_time, row, InpRequireExactBarTime);
   if(!found)
   {
      string status = DAL_AstroMapStore_LookupDiagnosticText(
         g_astro_store,
         bar_time,
         InpRequireExactBarTime,
         InpBrokerGmtOffsetHours
      );
      Print(status);
      if(InpUseTerminalComment)
         Comment(status);
      else if(InpClearChartComment)
         Comment("");
      if(InpUseObjectPanel)
         DAL_AstroMap_DrawStatus(0, "EXP0013", status, InpPanelX, InpPanelY, clrTomato);
      return;
   }

   if(InpValidateUtcOffset && !DAL_AstroMapRow_ValidateUtcOffset(row, InpBrokerGmtOffsetHours, 2))
   {
      string bad = "ASTRO UTC OFFSET MISMATCH\n";
      bad += "broker=" + TimeToString(row.broker_time, TIME_DATE | TIME_MINUTES) + "\n";
      bad += "row utc=" + TimeToString(row.utc_time, TIME_DATE | TIME_MINUTES) + "\n";
      bad += "input gmt offset=" + DoubleToString(InpBrokerGmtOffsetHours, 2);
      if(InpUseTerminalComment)
         Comment(bad);
      else if(InpClearChartComment)
         Comment("");
      if(InpUseObjectPanel)
         DAL_AstroMap_DrawStatus(0, "EXP0013", bad, InpPanelX, InpPanelY, clrTomato);
      return;
   }

   if(InpShowDerivedFeatureKey)
   {
      string compact = DAL_AstroDF_BuildCompactExecutionKey(row);
      string research = DAL_AstroDF_BuildResearchKey(row);
      Print("EXP0013 ASTRO bar=", TimeToString(bar_time, TIME_DATE | TIME_MINUTES),
            " compact=", compact,
            " research=", research);
   }

   if(InpClearChartComment && !InpUseTerminalComment)
      Comment("");
   if(InpUseObjectPanel)
      DAL_AstroMap_DrawPanel(0, "EXP0013", row, InpPanelX, InpPanelY, clrWhite);
}
