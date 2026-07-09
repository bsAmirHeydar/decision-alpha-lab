# Hunt Is Touch, Not Close

A hunt exists when price touches or breaks a reference through the high/low path.

High hunt:

```text
current_cycle_high >= reference_high
```

Low hunt:

```text
current_cycle_low <= reference_low
```

Close beyond the reference is not required. This is a core doctrine inherited from the strategy-architect answers.
