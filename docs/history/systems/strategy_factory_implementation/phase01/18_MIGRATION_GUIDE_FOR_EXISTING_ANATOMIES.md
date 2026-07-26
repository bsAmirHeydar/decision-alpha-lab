# Migration Guide for Existing Anatomies

## EXP0017

Map current divergence ledger rows to AnatomyEvent. Preserve hunter/clean symbols, cycle group, reference age, and divergence strength as FeatureValues. Do not place outcome fields in the event.

## NDS / Hook / F / Zone

Each canonical lifecycle transition can emit an AnatomyEvent. Hook ID, sequence ID, F state, parent hook, zone ID, and validity state become versioned features or parent relationships. The event ID must not depend on visual labels.

## Structural nodes

A node creation, first touch, revisit, rejection, acceptance, or retirement can be an anatomy event. Node geometry and source node ID should be preserved in source hash or features.

## Daye

Cycle boundaries and references use MarketTimestamp. Timezone conversion belongs to the later market-clock service; Daye adapters must not emit terminal-local ambiguous times.

## Astro

Astro state is a feature source, not a separate time system. Candle alignment and ephemeris source version are mandatory lineage.

## Migration pattern

```text
Existing engine output
  -> thin adapter
  -> SF01_AnatomyEvent
  -> validation
  -> golden fixture
  -> differential replay against old output
```
