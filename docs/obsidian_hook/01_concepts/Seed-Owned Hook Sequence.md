# Seed-Owned Hook Sequence

A seed-owned Hook sequence starts from the first raw same-side node that has not participated in earlier accepted sequences.

For positive Hooks the raw list is valleys. For negative Hooks the raw list is peaks.

The sequence is extended forward to the end of the raw list. It does not stop at node 2 when later strict continuation nodes exist.
