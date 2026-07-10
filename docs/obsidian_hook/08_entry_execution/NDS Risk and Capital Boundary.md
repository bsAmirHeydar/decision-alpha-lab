# NDS Risk and Capital Boundary

## Principle

Convex geometry does not authorize capital. Position sizing is an independent decision system.

## Required future inputs

```text
account equity authority
risk budget per Setup
symbol tick size/value
contract size
currency conversion
volume minimum/maximum/step
aggregate open risk
correlated exposure
daily and strategy loss limits
portfolio kill switch
```

## Required outputs

```text
risk_authorization_id
approved_risk_fraction
approved_volume
normalization evidence
portfolio impact
approval/rejection reason
expiry
```

## Current implementation

No capital model is active. Every Trade Plan and Command Preview carries zero requested volume.

## Separation

Risk code may reject or reduce a Setup. It must not relabel a Hook, move a Zone, or invent a target.

## Related

- [[NDS Authority Boundary]]
- [[NDS Trade Plan Contract]]
