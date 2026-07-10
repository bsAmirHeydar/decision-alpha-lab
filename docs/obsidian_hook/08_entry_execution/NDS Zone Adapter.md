# NDS Zone Adapter

## Single implementation seam

```text
FP_NDSBuildCanonicalZoneAdapter(...)
```

All final Hook-to-Zone geometry must be implemented here or in modules called exclusively by this adapter. Setup, risk, renderer, and broker code must not independently invent Zone boundaries.

## Current behavior

The canonical adapter deliberately returns:

```text
NDS_ZONE_CANON_ADAPTER_PENDING
canonical = false
available = false
```

until the Zone questionnaire locks:

- source points;
- upper/lower boundary rules;
- wick/close/node semantics;
- padding and width limits;
- birth, activation, touch, consumption, invalidation, and expiry;
- entry, stop, target, and trade-direction contracts.

## Diagnostic profile

Manual Zone, entry, stop, and target prices can exercise the downstream pipeline. The profile remains non-canonical and no-send. Entry must lie inside the manually supplied Zone and the directional geometry must be coherent.

## Related

- [[NDS Entry Canon Backlog]]
- [[NDS Setup State Machine]]
