# 03 — FF XML Parser Contract

The parser reads `<event>` blocks and extracts:

```text
title
country
date
time
impact
actual
forecast
previous
url
```

## Parser Rules

- invalid date rows are skipped
- missing title/country/date rows are skipped
- all-day rows are included only when `InpParserIncludeAllDay=true`
- tentative rows are placed at 12:00 source time unless explicit time exists
- impact text maps to internal impact constants
- country maps to currency code
- source time goes through Stage 03 conversion

## Parser Diagnostics

Runtime fields:

```text
runtime.parser_blocks_seen
runtime.parser_events_added
runtime.parser_events_skipped
runtime.parser_last_summary
runtime.parser_last_warning
```
