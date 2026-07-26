---
id: EXP0018-P05-ENTITIES
title: "P05 Domain Entities and Identities"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# Domain Entities

- **Hunt Side:** `HIGH` or `LOW`; not a trade direction.
- **Symbol Hunt Fact:** one symbol, one side, one current/reference pair.
- **Hunt Observation:** both symbol facts for one P04 opportunity and one side.
- **Pair State:** `NONE`, `A_ONLY`, `B_ONLY`, `BOTH`, `UNAVAILABLE`.

## Deterministic identity

`EXP0018|P05|<P04 opportunity id>|<HIGH or LOW>`

The identity excludes current price because price changes must update the same observation rather than create unstable duplicates.
