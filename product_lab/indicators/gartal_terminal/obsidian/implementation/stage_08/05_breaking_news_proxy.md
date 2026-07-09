# 05 — Breaking News Proxy

Stage 08 does not yet implement a true real-time headline stream.

It marks scheduled or calendar-included special events as breaking when titles contain tokens such as:

```text
Trump
President speaks
Emergency
Unscheduled
President statement
```

This makes such events participate in:

- breaking filter
- red visual emphasis
- breaking alert path
- dashboard breaking metric

True sudden headline ingestion is a future source adapter, not part of weekly XML parsing.
