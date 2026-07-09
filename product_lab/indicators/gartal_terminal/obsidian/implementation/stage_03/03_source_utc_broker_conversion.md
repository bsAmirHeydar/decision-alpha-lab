# 03 — Source / UTC / Broker Conversion

## Canonical flow

```text
Source time -> UTC -> Broker time -> optional emergency shift
```

## Source modes

| Mode | Value | Meaning |
|---|---:|---|
| UTC | 0 | Source timestamp is already UTC |
| Broker | 1 | Source timestamp is already broker time |
| Manual Source GMT | 2 | Source timestamp is in a manually configured timezone |

## Functions

```text
GT_SourceToUtcTime()
GT_UtcToBrokerTime()
GT_SourceToBrokerTime()
GT_BrokerToUtcTime()
GT_BrokerToSourceTime()
GT_UpdateEventTimeFields()
```

## Emergency shift

`InpTimeShiftMinutes` is applied after normal conversion. This exists for emergency field correction only, not as the primary configuration method.

## Future Forex Factory integration

The Stage 08 parser should not decide chart time. It should parse a source timestamp and call either:

```text
GT_AddEventFromSource(...)
```

or, if the parsed timestamp is known to be UTC:

```text
GT_AddEventFromUtc(...)
```

The store then produces `event.time_broker`.
