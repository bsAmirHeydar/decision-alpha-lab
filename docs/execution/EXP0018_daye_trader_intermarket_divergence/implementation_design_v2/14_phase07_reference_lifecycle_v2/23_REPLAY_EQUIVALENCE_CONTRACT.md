# Replay equivalence contract

P11 must call the same lifecycle transitions in event-time order. Replay may reconstruct history from source bars; live P07 may not fabricate missed ordering after checkpoint loss.

Equivalence key:

```text
reference id + terminal state + retirement evidence id
accepted use ids in chronological order
```
