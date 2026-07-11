# MQL5 API Reference

## Include entry point

```mql5
#include <AlphaLab\StrategyFactory\Contracts\SF01_AllContracts.mqh>
```

## Typical AnatomyEvent construction

```mql5
SF01_AnatomyEvent event;
event.schema = SF01_AnatomyEventSchema();
event.strategy_id = "exp0017_temporal_divergence";
event.strategy_version = "1.0.0";
event.producer_id = "mql5.exp0017.adapter";
event.producer_version = "1.0.0";
event.symbol = _Symbol;
event.reference_symbol = "ES";
event.direction = SF01_DIRECTION_LONG;
event.event_time = SF01_MakeUtcTimestamp(event_bar_time, "broker", broker_offset, "broker");
event.known_time = SF01_MakeUtcTimestamp(known_bar_time, "broker", broker_offset, "broker");
event.confirmation_time = SF01_MakeUtcTimestamp(confirmation_bar_time, "broker", broker_offset, "broker");
event.market_event_cluster_id = cluster_id;
event.source_hash = source_hash;
event.event_id = SF01_DeriveAnatomyEventId(event);

string error = "";
if(!SF01_ValidateAnatomyEvent(event, error))
{
   Print("Rejected anatomy event: ", error);
   return;
}
```

## Snapshot construction

Initialize snapshot metadata first, because `Add` checks feature known time against snapshot time. Add each feature once. Derive the snapshot ID only after the feature set is complete. Validate before passing it to any later module.

## Error handling

All validators use `bool` plus an output error string. Callers must not ignore `false`. The expected runtime action is quarantine or abstention. Logging the error and continuing with the object is forbidden.

## Allocation notes

Avoid rebuilding large snapshots on every tick. Later context modules should update state incrementally and create a snapshot only when an anatomy event requires a decision or research capture.
