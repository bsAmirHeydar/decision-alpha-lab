#property strict
#property version   "1.00"
#property description "EXP0013 Astro Feature Store visual/tester demo. Research-only; sends no orders."

#include <Research/DAL_AstroFeatureStore.mqh>
#include <Research/DAL_AstroDistributionAdapter.mqh>

input string          InpAstroCsvFile          = "astro/astro_features.csv";
input ENUM_TIMEFRAMES InpChartTimeframe        = PERIOD_M1;
input int             InpBrokerGmtOffsetHours  = 0;
input bool            InpRequireExactBarTime   = true;
input bool            InpDrawPanel             = true;
input bool            InpPrintOnNewBar         = true;

DAL_AstroFeatureStore g_astro_store;
datetime g_last_bar_time = 0;

int OnInit()
{
   bool ok = DAL_AstroFeatureStore_LoadCsv(g_astro_store, InpAstroCsvFile, InpBrokerGmtOffsetHours);
   if(!ok)
   {
      Print("EXP0013 failed to load astro CSV: ", InpAstroCsvFile);
      return INIT_FAILED;
   }

   Print("EXP0013 loaded astro store rows=", g_astro_store.row_count, " file=", InpAstroCsvFile);
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   ObjectDelete(0, "EXP0013_ASTRO_PANEL");
   Comment("");
}

void OnTick()
{
   datetime bar_time = iTime(_Symbol, InpChartTimeframe, 0);
   if(bar_time <= 0)
      return;

   if(bar_time == g_last_bar_time)
      return;
   g_last_bar_time = bar_time;

   DAL_AstroFeatureRow row;
   bool found = DAL_AstroFeatureStore_FindByBrokerTime(
      g_astro_store,
      bar_time,
      row,
      InpRequireExactBarTime
   );

   if(!found)
   {
      string st = "ASTRO FEATURE STORE\nmissing row for broker bar: " + TimeToString(bar_time, TIME_DATE | TIME_MINUTES) +
                  "\nfile=" + InpAstroCsvFile +
                  "\nCheck broker GMT offset and CSV date range.";
      if(InpDrawPanel)
         DAL_Astro_DrawStatus(0, "EXP0013", st);
      Comment(st);
      if(InpPrintOnNewBar)
         Print(st);
      return;
   }

   string dist_key = DAL_Astro_AppendToDistributionKey("demo_symbol=" + _Symbol, row, true);

   if(InpDrawPanel)
      DAL_Astro_DrawPanel(0, "EXP0013", row);

   Comment(DAL_AstroFeatureRow_ToMultilineText(row));

   if(InpPrintOnNewBar)
   {
      Print("EXP0013_ASTRO bar=", TimeToString(bar_time, TIME_DATE | TIME_MINUTES),
            " utc=", TimeToString(row.utc_time, TIME_DATE | TIME_MINUTES),
            " key=", row.feature_key,
            " dist_key=", dist_key);
   }
}
