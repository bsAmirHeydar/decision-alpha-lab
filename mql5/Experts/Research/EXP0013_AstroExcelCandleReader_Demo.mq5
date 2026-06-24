#property strict
#property version   "1.00"
#property description "EXP0013 Astro Excel/CSV Candle Reader Demo"
#property description "Loads Python-generated candle-aligned astro CSV and displays the sky map per candle."

#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroDerivedFeatures.mqh>

input string          InpAstroCsvFile            = "astro\\astro_XAUUSD_M1_202401_mql.csv";
input double          InpBrokerGmtOffsetHours    = 2.0;
input ENUM_TIMEFRAMES InpReadTimeframe           = PERIOD_M1;
input bool            InpRequireExactBarTime     = true;
input bool            InpReadOnlyOnNewBar        = true;
input bool            InpValidateUtcOffset       = true;
input bool            InpShowDerivedFeatureKey   = true;

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
      Print("EXP0013 failed to load astro CSV. Put the CSV in MQL5/Files/", InpAstroCsvFile);
      return INIT_FAILED;
   }

   Print("EXP0013 Astro reader initialized. rows=", g_astro_store.row_count,
         " file=", InpAstroCsvFile,
         " broker_gmt_offset=", DoubleToString(InpBrokerGmtOffsetHours, 2));
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   ObjectDelete(0, "EXP0013_ASTRO_MAP_PANEL");
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
      string status = "ASTRO MAP NOT FOUND\n";
      status += "file=" + InpAstroCsvFile + "\n";
      status += "bar=" + TimeToString(bar_time, TIME_DATE | TIME_MINUTES) + "\n";
      status += "exact=" + (InpRequireExactBarTime ? "true" : "false");
      DAL_AstroMap_DrawStatus(0, "EXP0013", status, 10, 20, clrYellow);
      return;
   }

   if(InpValidateUtcOffset && !DAL_AstroMapRow_ValidateUtcOffset(row, InpBrokerGmtOffsetHours, 2))
   {
      string bad = "ASTRO UTC OFFSET MISMATCH\n";
      bad += "broker=" + TimeToString(row.broker_time, TIME_DATE | TIME_MINUTES) + "\n";
      bad += "row utc=" + TimeToString(row.utc_time, TIME_DATE | TIME_MINUTES) + "\n";
      bad += "input gmt offset=" + DoubleToString(InpBrokerGmtOffsetHours, 2);
      DAL_AstroMap_DrawStatus(0, "EXP0013", bad, 10, 20, clrTomato);
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

   DAL_AstroMap_DrawPanel(0, "EXP0013", row, 10, 20, clrWhite);
}
