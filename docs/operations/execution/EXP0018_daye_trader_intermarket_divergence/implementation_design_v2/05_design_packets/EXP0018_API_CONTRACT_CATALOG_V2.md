  ---
  id: EXP0018-API-CATALOG-V2
  title: "EXP0018 API Contract Catalog v2"
  type: api-contract
  status: draft
  project: EXP0018
  version: 2.0.0
  created: 2026-07-10
  updated: 2026-07-10
  tags:
    - exp0018
- daye-trader
- implementation-design
  ---

# کاتالوگ API پیشنهادی

```text
TimeEngine.Resolve(broker_time) -> DayeTimePoint
DataSync.BuildFrame(time_range) -> SyncFrameResult
PeriodStore.Build(sync_frame, period_type) -> PeriodSnapshot[]
SignalRegistry.Resolve(instance_time) -> SignalDefinition[]
HuntDetector.Observe(definition, reference, current) -> HuntObservation
Confirmation.Apply(closed_bar_event, observations) -> ConfirmationEvent[]
Lifecycle.Apply(event) -> ReferenceTransition
VisualEvent.From(confirmation, lifecycle_snapshot) -> VisualEvent
Drawing.Render(chart_id, visual_event) -> RenderResult
Replay.Run(range) -> ReplayManifest
Ledger.Append(event) -> WriteResult
```

هر API باید status صریح، reason code و input identity برگرداند.
