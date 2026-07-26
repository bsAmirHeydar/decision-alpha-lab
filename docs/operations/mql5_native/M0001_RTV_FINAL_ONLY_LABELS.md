# M0001 RTV Final-Only Labels

RTV is now treated as a final statistic only.

A chart label is drawn only when:

```text
event.rtv_ready == true
```

That means the event must first close by `exit_gap` consecutive candles whose
high/low do not intersect the frozen event zone. Until that closure happens, no
RTV label is shown.

This removes unfinished labels such as:

```text
RTV n/a
```

RTV summary mean/median and the text export were already based only on ready RTV
events; this change makes the chart labels follow the same final-only rule.

Version: `1.51`
