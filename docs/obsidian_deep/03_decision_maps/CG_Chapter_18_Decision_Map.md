# CG Chapter 18 Decision Map

```text
Confirmed divergence?
  No -> no trade permission
  Yes -> did clean symbol hunt its reference by final confirmation?
      Yes -> divergence invalidated
      No -> trade permission
          Existing positions? -> ignored in base layer
          Same CG positions? -> ignored in base layer
          Hedge conflict? -> allowed in base layer
          Prior loss? -> ignored in base layer
          Prior win? -> ignored in base layer
          Entry -> immediately after final confirmation
```

## Key decision boundary

Only invalidation blocks execution in the base layer.
