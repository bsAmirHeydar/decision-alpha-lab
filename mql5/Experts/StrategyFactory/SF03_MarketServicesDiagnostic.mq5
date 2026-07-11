#property strict
#property version "1.00"
#property description "Phase 03 market service diagnostic. No order authority."

#include <AlphaLab\StrategyFactory\Core\SF02_AllCore.mqh>
#include <AlphaLab\StrategyFactory\Market\SF03_AllMarket.mqh>

input string InpSymbol="";
input ENUM_TIMEFRAMES InpTimeframe=PERIOD_M1;
input int InpBrokerUtcOffsetMinutes=0;
input int InpHistoryBars=128;
input int InpRefreshSeconds=1;

CSF03MarketServiceBundle g_services;
string g_symbol="";
int g_timeframe_seconds=60;

int OnInit()
{
   g_symbol=(InpSymbol=="")?_Symbol:InpSymbol;
   g_timeframe_seconds=PeriodSeconds(InpTimeframe);
   if(g_timeframe_seconds<=0)
   {
      Print("Invalid timeframe");
      return INIT_FAILED;
   }

   SF02_RuntimeConfig runtime_config=SF02_DefaultRuntimeConfig();
   runtime_config.strategy_id="sf03_market_diagnostic";
   runtime_config.strategy_version="1.0.0";
   runtime_config.run_id="sf03_market_diagnostic_run";

   SF03_ClockConfig clock_config;
   clock_config.mode=SF03_CLOCK_SERVER_FIXED_OFFSET;
   clock_config.broker_utc_offset_minutes=InpBrokerUtcOffsetMinutes;
   clock_config.broker_timezone_id="broker_fixed";
   clock_config.source_clock_id="sf03_terminal";
   clock_config.strict_offset_validation=true;

   string error="";
   if(!g_services.Initialize(runtime_config,clock_config,error))
   {
      Print("Initialize failed: ",error);
      return INIT_FAILED;
   }
   if(!g_services.Start(error))
   {
      Print("Start failed: ",error);
      return INIT_FAILED;
   }
   if(!g_services.Market().RegisterSeries(g_symbol,g_timeframe_seconds,error))
   {
      Print("Register series failed: ",error);
      return INIT_FAILED;
   }

   const int refresh_seconds=(InpRefreshSeconds<1)?1:InpRefreshSeconds;
   EventSetTimer(refresh_seconds);
   PrintFormat("SF03 diagnostic ready symbol=%s timeframe_seconds=%d",
               g_symbol,g_timeframe_seconds);
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_services.Stop();
   g_services.Shutdown();
}

void OnTick()
{
   string error="";
   MqlTick tick;
   if(!g_services.Market().LatestTick(g_symbol,tick,error))
      Print("LatestTick: ",error);
}

void OnTimer()
{
   string error="";
   const int copied=g_services.Market().RefreshSeries(
      g_symbol,g_timeframe_seconds,((InpHistoryBars<3)?3:InpHistoryBars),error
   );
   if(copied<=0)
   {
      Print("RefreshSeries: ",error);
      return;
   }

   SF01_BarRecord bar;
   if(!g_services.Market().LatestClosedBar(g_symbol,g_timeframe_seconds,bar,error))
   {
      Print("LatestClosedBar: ",error);
      return;
   }

   SF02_SymbolSpec spec;
   if(!g_services.Specs().Get(g_symbol,spec,error))
   {
      Print("SymbolSpec: ",error);
      return;
   }

   PrintFormat(
      "SF03 market healthy symbol=%s close_utc_msc=%I64d close=%.8f generation=%I64d tick_size=%.8f",
      g_symbol,
      bar.close_time.utc_epoch_milliseconds,
      bar.close_price,
      g_services.Market().SeriesGeneration(g_symbol,g_timeframe_seconds),
      spec.tick_size
   );
}
