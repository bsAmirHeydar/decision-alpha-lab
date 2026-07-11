#property strict
#property version "1.00"
#property description "Strategy Factory Phase 02 runtime self-test; no order authority"

#include <AlphaLab\StrategyFactory\Runtime\SF02_AllRuntime.mqh>
#include <AlphaLab\StrategyFactory\Adapters\Null\SF02_NoSendExecutionBoundary.mqh>
#include <AlphaLab\StrategyFactory\Testing\SF02_Assert.mqh>
#include <AlphaLab\StrategyFactory\Testing\SF02_FixtureServices.mqh>

int OnInit()
{
   CSF02Assert assert;
   string error = "";

   SF02_RuntimeConfig config = SF02_DefaultRuntimeConfig();
   config.strategy_id = "fixture_strategy";
   config.strategy_version = "1.0.0";
   config.run_id = "run_phase02_selftest";
   config.run_mode = SF02_MODE_ANATOMY_AUDIT;
   config.max_events_per_cycle = 4;
   config.audit_bus_capacity = 16;

   assert.True(SF02_ValidateRuntimeConfig(config, error), "runtime config validates");

   CSF02TypedEventBus bus;
   assert.True(bus.Initialize(8, SF02_BUS_REJECT_NEW, error), "typed bus initializes");
   SF02_EventEnvelope envelope;
   envelope.sequence = 0;
   envelope.event_type = SF02_EVENT_HEARTBEAT;
   envelope.aggregate_id = "runtime_fixture";
   envelope.source_id = "selftest";
   envelope.occurred_at = SF01_MakeUtcMilliseconds(1000, "UTC", 0, "fixture", SF01_TIME_MILLISECONDS);
   envelope.known_at = envelope.occurred_at;
   envelope.payload_hash = "sha256_fixture";
   envelope.priority = 10;
   assert.True(bus.Publish(envelope, error), "typed bus publish");
   SF02_EventEnvelope polled;
   assert.True(bus.Poll(polled), "typed bus poll");
   assert.True(polled.sequence == 1, "typed bus sequence starts at one");

   CSF02FixtureClock clock;
   CSF02FixtureAnatomyProvider anatomy;
   CSF02FixtureFeatureProvider features;
   CSF02FixtureSink sink;
   CSF02NoSendExecutionBoundary execution_boundary;
   CSF02StrategyRuntime runtime;

   runtime.BindClock(&clock);
   runtime.BindAnatomy(&anatomy);
   runtime.BindFeatures(&features);
   runtime.BindSink(&sink);
   runtime.BindExecutionBoundary(&execution_boundary);

   assert.True(runtime.Initialize(config, error), "runtime initializes");
   assert.True(runtime.State() == SF02_STATE_READY, "runtime reaches READY");
   assert.True(runtime.Start(error), "runtime starts");
   assert.True(runtime.State() == SF02_STATE_RUNNING, "runtime reaches RUNNING");

   MqlTick tick;
   ZeroMemory(tick);
   tick.time = 1783771260;
   tick.bid = 22500.0;
   tick.ask = 22500.25;
   assert.True(runtime.OnTick(tick, error), "runtime processes fixture tick");
   assert.True(runtime.ProcessedEvents() == 1, "one event processed");
   assert.True(runtime.CreatedSnapshots() == 1, "one snapshot created");
   assert.True(sink.Events() == 1, "sink received event");
   assert.True(sink.Snapshots() == 1, "sink received snapshot");
   assert.True(!execution_boundary.HasLiveOrderAuthority(), "execution authority remains disabled");

   assert.True(runtime.Stop(error), "runtime stops");
   assert.True(runtime.State() == SF02_STATE_STOPPED, "runtime reaches STOPPED");
   runtime.Shutdown();

   Print("SF02 SELFTEST passed=", assert.Passed(), " failed=", assert.Failed());
   return assert.Failed() == 0 ? INIT_SUCCEEDED : INIT_FAILED;
}
