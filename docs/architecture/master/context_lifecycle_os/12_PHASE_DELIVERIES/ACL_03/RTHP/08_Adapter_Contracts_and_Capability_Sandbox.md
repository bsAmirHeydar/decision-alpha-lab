---
title: RTHP Adapter Contracts and Capability Sandbox
status: contracts-compiled
version: 1.0.2
---
# Adapter Contracts and Capability Sandbox

ACL-03 generated five least-privilege adapter contracts from the two tick sources, one New York calendar, and two feature views.

## Contract status

All central adapter artifacts remain `CONTRACT_ONLY`. This is intentional. ACL-03 proves interfaces and capabilities, not production adapter implementation.

## Capability restrictions

- Network egress is denied by default or absent.
- Filesystem writes are limited to declared cache/output locations.
- Secret access is absent or restricted to named secrets.
- Order submission is false.
- Capital access is false.
- Dynamic execution is forbidden.

## Open obligation

`ACL03_ADAPTER_IMPLEMENTATION_REQUIRED`

Later runtime work must implement and qualify adapters against these exact contracts. It may not broaden Context semantics.
