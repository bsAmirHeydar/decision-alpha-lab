---
type: architecture
product: gartal terminal
status: active
language: en
tags:
  - forex-factory
  - parser
  - html
---

# 04 — Forex Factory Parsing Contract

## Goal

Define a parser that converts Forex Factory style economic-calendar rows into canonical `GT_NewsEvent` records.

This document does not assume a permanent HTML structure. It defines the extraction contract and fallback logic.

## Required Fields

Every parsed event should attempt to populate:

| Canonical Field | Source Meaning | Required? |
|---|---|---:|
| `source_date` | calendar day | yes |
| `source_time` | event time shown on source | yes, except all-day holiday |
| `currency` | currency code such as USD/EUR/GBP | yes |
| `impact` | low/medium/high/holiday | yes |
| `title` | event name | yes |
| `actual` | actual value | no |
| `forecast` | forecast value | no |
| `previous` | previous value | no |
| `is_tentative` | tentative time flag | no |
| `is_speech` | speech/speaker event flag | no |
| `is_breaking` | breaking/unplanned flag | no |
| `is_revised` | revised previous/actual flag | no |

## Parser Layers

The parser should be split internally into these private functions:

```cpp
bool GT_ParseCalendarRows(const string payload, GT_RawCalendarRow &rows[], int &row_count);
bool GT_ParseRowDate(...);
bool GT_ParseRowTime(...);
bool GT_ParseRowCurrency(...);
bool GT_ParseRowImpact(...);
bool GT_ParseRowTitle(...);
bool GT_ParseRowValues(...);
bool GT_ParseRowFlags(...);
bool GT_MapRawRowToEvent(...);
```

## Impact Mapping

The parser must map source impact into canonical enum:

| Source Concept | Canonical Impact | Visual Meaning |
|---|---|---|
| low impact | `GT_IMPACT_LOW` | yellow/soft |
| medium impact | `GT_IMPACT_MEDIUM` | orange |
| high impact | `GT_IMPACT_HIGH` | red |
| holiday/non-economic | `GT_IMPACT_HOLIDAY` | gray |
| speech with high source impact | `GT_IMPACT_HIGH` + `is_speech=true` | red speech |
| breaking political item | `GT_IMPACT_HIGH` + `is_breaking=true` | red breaking |

## Event ID Contract

The parser must produce deterministic IDs.

Format:

```text
GT-{YYYYMMDD}-{HHMM_OR_ALLDAY}-{CURRENCY}-{IMPACT}-{TITLE_HASH}
```

Examples:

```text
GT-20260709-1530-USD-HIGH-NFPHASH
GT-20260709-ALLDAY-JPY-HOLIDAY-BANKHOLIDAYHASH
```

## Time Parsing Rules

### Explicit Time

```text
8:30am -> source day + source time
14:00 -> source day + source time
```

### Tentative

Tentative events should not receive a false precise minute unless the source exposes one.

Preferred model:

```cpp
is_tentative = true;
time_precision = GT_TIME_PRECISION_TENTATIVE;
```

If no precision enum exists yet, store as a best-effort time but mark `is_tentative=true` and render with a dashed/soft style.

### All Day

All-day events such as holidays should use a canonical display bucket rather than a hard false release minute.

First version can place all-day items at session open or dashboard-only.

## Actual / Forecast / Previous Rules

- Empty values are allowed.
- Non-breaking spaces and HTML entities must be normalized.
- Revised values should set `is_revised=true` if a revision marker is detected.
- Numeric conversion is not required for V1; preserve source string.

## Speech Detection

A row should be flagged as speech if title or metadata indicates:

```text
speaks
speech
testifies
testimony
press conference
statement
remarks
```

The list must be centralized and configurable later.

## Breaking Detection

A row should be flagged as breaking only when the source exposes unplanned/breaking markers or a secondary source mode marks it as breaking.

Do not infer breaking status purely from a political name.

## Parser Error Handling

Parser should return:

```cpp
bool success;
string error_message;
int parsed_count;
int rejected_count;
```

Rejected rows should not crash the product.

## Parser Test Dataset

The architecture requires sample payloads for:

1. normal high/medium/low calendar rows;
2. speech row;
3. tentative row;
4. holiday row;
5. row with missing actual;
6. row with revised previous;
7. malformed row;
8. duplicate row;
9. non-USD currency row;
10. dense red-news day.

## Acceptance Gate

Parser is not accepted until:

- sample payload parses without network;
- malformed rows are rejected safely;
- event IDs are stable across repeated parses;
- impact mapping is correct;
- speech flags are correct;
- dashboard receives only canonical events, not raw HTML.
