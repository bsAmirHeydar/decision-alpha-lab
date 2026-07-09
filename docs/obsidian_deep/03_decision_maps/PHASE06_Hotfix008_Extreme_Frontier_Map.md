# Decision Map — Hotfix008 Extreme Frontier

```text
Previous reference candidate
        |
        v
Was there a later equal/higher high for high-side?
        | yes -> suppress high-side reference
        | no
        v
Was there a later equal/lower low for low-side?
        | yes -> suppress low-side reference
        | no
        v
Reference remains eligible for divergence comparison
```
