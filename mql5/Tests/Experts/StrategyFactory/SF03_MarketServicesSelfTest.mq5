#property strict
#property version "1.00"
#property description "Strategy Factory Phase 03 shared market services self-test"

#include <AlphaLab\StrategyFactory\Contracts\SF01_AllContracts.mqh>
#include <AlphaLab\StrategyFactory\Core\SF02_AllCore.mqh>
#include <AlphaLab\StrategyFactory\Testing\SF02_Assert.mqh>
#include <AlphaLab\StrategyFactory\Market\SF03_AllMarket.mqh>
#include <AlphaLab\StrategyFactory\Testing\SF03_FixtureMarketSource.mqh>

int OnInit()
{
   CSF02Assert check;
   string error="";

   SF02_RuntimeConfig runtime_config=SF02_DefaultRuntimeConfig();
   runtime_config.strategy_id="sf03_self_test";
   runtime_config.strategy_version="1.0.0";
   runtime_config.run_id="sf03_self_test_run";

   SF03_ClockConfig clock_config;
   clock_config.mode=SF03_CLOCK_FIXTURE;
   clock_config.broker_utc_offset_minutes=120;
   clock_config.broker_timezone_id="broker_eet";
   clock_config.source_clock_id="sf03_fixture_clock";
   clock_config.strict_offset_validation=true;

   CSF03TimeKernel clock;
   clock.Configure(clock_config);
   clock.SetFixtureUtcMilliseconds(SF03_MakeUtcMilliseconds(2026,7,11,14,30,0));

   check.True(clock.Initialize(runtime_config,error),"time kernel initialize");
   check.True(clock.Start(error),"time kernel start");
   check.True(clock.NewYorkUtcOffsetMinutes(SF03_MakeUtcMilliseconds(2026,1,15,12,0,0))==-300,
              "new york winter offset");
   check.True(clock.NewYorkUtcOffsetMinutes(SF03_MakeUtcMilliseconds(2026,7,15,12,0,0))==-240,
              "new york summer offset");

   CSF03SessionSchedule sessions;
   SF03_SessionDefinition ny_am;
   ny_am.session_id="new_york_am";
   ny_am.enabled=true;
   ny_am.timezone_kind=SF03_TZ_NEW_YORK;
   ny_am.fixed_offset_minutes=0;
   ny_am.start_minute_of_day=570;
   ny_am.end_minute_of_day=720;
   ny_am.weekday_mask=62;
   check.True(sessions.Add(ny_am,error),"session add");

   SF03_SessionMatch match;
   check.True(sessions.Resolve(SF03_MakeUtcMilliseconds(2026,7,13,14,0,0),clock,match),
              "new york session match");
   check.True(match.session_id=="new_york_am","session identity");

   CSF03FixtureMarketSource source;
   const string symbol="#NQ";
   check.True(source.EnsureSymbol(symbol,error),"broker symbol accepted");

   MqlTick tick;
   ZeroMemory(tick);
   tick.time=(datetime)(clock.UtcNowMilliseconds()/1000L);
   tick.time_msc=clock.UtcNowMilliseconds();
   tick.bid=22500.00;
   tick.ask=22500.25;
   tick.last=22500.25;
   tick.volume=10;
   tick.volume_real=10.0;
   check.True(source.PutTick(symbol,tick,error),"fixture tick");

   const long base=SF03_MakeUtcMilliseconds(2026,7,11,14,25,0);
   check.True(source.PutBar(SF03_MakeFixtureBar(symbol,60,base,22499.0,22501.0,22498.5,22500.0),error),
              "bar one");
   check.True(source.PutBar(SF03_MakeFixtureBar(symbol,60,base+60000L,22500.0,22502.0,22499.5,22501.0),error),
              "bar two");
   check.True(source.PutBar(SF03_MakeFixtureBar(symbol,60,base+120000L,22501.0,22503.0,22500.5,22502.0),error),
              "bar three");
   check.True(source.PutSpec(SF03_MakeFixtureSpec(symbol,clock.UtcNowMilliseconds()),error),
              "fixture spec");

   CSF03MarketDataService market;
   market.BindSource(&source);
   market.BindClock(&clock);
   market.Configure(5000,64,SF03_MISSING_FAIL_CLOSED);
   check.True(market.Initialize(runtime_config,error),"market initialize");
   check.True(market.Start(error),"market start");
   check.True(market.RefreshTick(symbol,error),"tick refresh");
   check.True(market.RefreshSeries(symbol,60,3,error)==3,"bar refresh count");

   MqlTick cached_tick;
   check.True(market.LatestTick(symbol,cached_tick,error),"latest tick");
   check.True(cached_tick.bid==tick.bid,"cached tick value");

   SF01_BarRecord latest;
   check.True(market.LatestClosedBar(symbol,60,latest,error),"latest closed bar");
   check.True(latest.close_price==22502.0,"latest bar close");
   check.True(market.IsSynchronized(symbol,60),"single series synchronized");

   CSF03NewBarTracker tracker;
   bool is_new=false;
   check.True(tracker.Observe(latest,is_new,error) && is_new,"new bar first observation");
   is_new=true;
   check.True(tracker.Observe(latest,is_new,error) && !is_new,"new bar duplicate rejected");

   CSF03SymbolSpecCache specs;
   specs.BindSource(&source);
   check.True(specs.Initialize(runtime_config,error),"spec cache initialize");
   check.True(specs.Start(error),"spec cache start");
   SF02_SymbolSpec compact_spec;
   check.True(specs.Get(symbol,compact_spec,error),"symbol spec get");
   check.True(compact_spec.tick_size==0.25,"symbol tick size");
   check.True(compact_spec.specification_generation>0,"spec generation");

   SF03_SyncRequirement requirements[1];
   requirements[0].symbol=symbol;
   requirements[0].timeframe_seconds=60;
   requirements[0].max_close_skew_milliseconds=0;
   requirements[0].max_staleness_milliseconds=600000;
   SF03_SyncResult sync_result;
   check.True(market.EvaluateSynchronization(requirements,sync_result,error),
              "single series synchronization");
   check.True(sync_result.status==SF03_SYNC_READY,"sync ready status");

   const SF03_MarketTelemetrySnapshot telemetry=market.Telemetry();
   check.True(telemetry.tick_updates==1,"telemetry tick update");
   check.True(telemetry.bar_insertions==3,"telemetry bar insertions");
   check.True(telemetry.source_errors==0,"telemetry source errors");

   specs.Stop();
   specs.Shutdown();
   market.Stop();
   market.Shutdown();
   clock.Stop();
   clock.Shutdown();

   PrintFormat("SF03 self-test complete: passed=%d failed=%d",check.Passed(),check.Failed());
   return check.Failed()==0 ? INIT_SUCCEEDED : INIT_FAILED;
}

void OnDeinit(const int reason) {}
void OnTick() {}
