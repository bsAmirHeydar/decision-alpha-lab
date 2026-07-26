---
title: "Parity Dimension Matrix"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Parity Dimension Matrix

| Dimension | Default severity | Default tolerance |
|---|---|---|
| known-time availability | hard | zero |
| closed/current bar selection | hard | zero |
| context state transition | hard | zero |
| setup decision and direction | hard | zero |
| invalidation/cancellation/expiry | hard | zero |
| reference consumption | hard | zero |
| reason-code meaning | hard | semantic exact |
| treatment request | hard | contract exact; numeric policy explicit |
| drawing anchor time/price | hard | zero bars; tick policy explicit |
| visual color/width | soft | approved style map |
| event ordering | hard | zero |
| replay determinism | hard | identical digest |
| processing latency | soft | phase budget |
| memory use | soft | phase budget |
