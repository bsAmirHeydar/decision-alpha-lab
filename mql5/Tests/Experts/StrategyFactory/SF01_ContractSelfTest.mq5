#property strict
#property version   "1.000"
#property description "Strategy Factory Phase 01 canonical contract self-test"

#include <AlphaLab\StrategyFactory\Contracts\SF01_AllContracts.mqh>

int g_failures = 0;

void SF01_Assert(const bool condition, const string label)
{
   if(condition)
      Print("[SF01][PASS] ", label);
   else
   {
      Print("[SF01][FAIL] ", label);
      g_failures++;
   }
}

SF01_AnatomyEvent SF01_TestEvent()
{
   SF01_AnatomyEvent value;
   value.schema = SF01_AnatomyEventSchema();
   value.event_id = "";
   value.strategy_id = "exp0017_temporal_divergence";
   value.strategy_version = "1.0.0";
   value.producer_id = "mql5.exp0017.adapter";
   value.producer_version = "1.0.0";
   value.symbol = "NQ";
   value.reference_symbol = "ES";
   value.direction = SF01_DIRECTION_LONG;
   value.event_time = SF01_MakeUtcMilliseconds(1783771200000, "America/New_York", -240, "broker", SF01_TIME_MILLISECONDS);
   value.known_time = SF01_MakeUtcMilliseconds(1783771260000, "America/New_York", -240, "broker", SF01_TIME_MILLISECONDS);
   value.confirmation_time = SF01_MakeUtcMilliseconds(1783771320000, "America/New_York", -240, "broker", SF01_TIME_MILLISECONDS);
   value.reference_price = 22500.25;
   value.invalidation_price = 22480.00;
   value.timeframe_seconds = 60;
   value.session_id = "new_york_am";
   value.parent_event_id = "none";
   value.market_event_cluster_id = "cluster_20260711_001";
   value.source_hash = "sha256_deadbeef";
   value.anatomy_state = "confirmed";
   return value;
}

int OnInit()
{
   string error = "";
   SF01_Assert(SF01_ContractKernelVersion() == "1.0.0", "kernel version");

   SF01_SchemaIdentity schema = SF01_AnatomyEventSchema();
   SF01_Assert(SF01_ValidateSchemaIdentity(schema, error), "schema validation");
   SF01_Assert(SF01_SchemaCanonical(schema) == "alpha_lab.strategy_factory/anatomy_event@1.0.0", "schema canonical form");

   SF01_AnatomyEvent event = SF01_TestEvent();
   const string derived = SF01_DeriveAnatomyEventId(event);
   SF01_Assert(derived == "evt_cd79492563408d2b", "cross-language event ID");
   event.event_id = derived;
   SF01_Assert(SF01_ValidateAnatomyEvent(event, error), "anatomy event validation");

   SF01_AnatomyEvent invalid_event = event;
   invalid_event.known_time.utc_epoch_milliseconds = invalid_event.confirmation_time.utc_epoch_milliseconds + 1;
   SF01_Assert(!SF01_ValidateAnatomyEvent(invalid_event, error), "future-time violation rejected");

   CSF01FeatureSnapshot snapshot;
   snapshot.schema = SF01_FeatureSnapshotSchema();
   snapshot.event_id = event.event_id;
   snapshot.strategy_id = event.strategy_id;
   snapshot.snapshot_time = event.confirmation_time;
   snapshot.producer_id = "mql5.context.exp0017";
   snapshot.producer_version = "1.0.0";
   snapshot.source_hash = "sha256_context";
   snapshot.state_generation = 7;
   SF01_FeatureValue feature = SF01_MakeDoubleFeature("divergence_strength", "1.0.0", 0.75,
                                                      event.known_time, event.event_id, "sha256_feature");
   SF01_Assert(snapshot.Add(feature, error), "feature addition");
   snapshot.snapshot_id = snapshot.DeriveId();
   SF01_Assert(snapshot.snapshot_id == "snap_a1483fb0aa370dc5", "cross-language snapshot ID");
   SF01_Assert(snapshot.Validate(error), "snapshot validation");
   SF01_Assert(!snapshot.Add(feature, error), "duplicate feature rejected");

   Print("[SF01] AnatomyEvent JSON: ", SF01_AnatomyEventToJson(event));
   Print("[SF01] Completed with failures=", g_failures);
   if(g_failures > 0) return INIT_FAILED;
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason) {}
void OnTick() {}
