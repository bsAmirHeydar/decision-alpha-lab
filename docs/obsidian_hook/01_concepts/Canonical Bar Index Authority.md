# Canonical Bar Index Authority

Structural ownership, ordering and distance in NDS are measured on the canonical closed-bar stream.

```text
rates[0] = oldest copied closed bar
higher index = newer closed bar
bar distance = newer_index - older_index
```

Timestamps remain useful for labels and exports, but they must not replace bar-index authority for:

- post-F3 ownership windows;
- terminal-origin tolerance in bars;
- candidate order;
- structural distance;
- historical reconstruction.

This avoids session-gap, missing-bar and chart-period distortions caused by converting a requested bar count into wall-clock seconds.
