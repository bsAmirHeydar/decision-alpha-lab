---
title: ACL-12 — Security Hardening
status: accepted-reference
version: 3.0.0
updated: 2026-07-18
tags: [acl-os, acl-12, security]
---
# ACL-12 — Security Hardening

ACL-12 consumes the immutable `ACL11_TO_ACL12` custody package and produces a deterministic security-control assessment, threat assessment, reference SBOM, dependency recall graph, scan evidence, operator-separation matrix, key-custody interface, incident and revocation contracts, risk register, evidence bundle and non-production readiness decision.

## Reference result

The upstream package contains zero runtime candidates and no generated runtime. ACL-12 preserves that state. Reference controls are hardened, but production readiness remains false because external attestations and operational evidence are absent.

## Required actions

- verify the complete ACL-11 package;
- apply the closed ACL-12 control and threat registries;
- preserve UNKNOWN as a production blocker;
- produce the `ACL12_TO_ACL13` handoff atomically.

## Forbidden actions

- invent runtime or security evidence;
- access or generate production key material;
- authorize runtime activation, live orders or capital;
- accept residual risk automatically;
- treat local scanning as production attestation.

## Claim ceiling

`SECURITY_HARDENING_REFERENCE_ONLY`

## Related

- [[ACL12_SECURITY_HARDENING_RUNTIME]]
- [[ACL12_SECURITY_EVIDENCE_BUNDLE]]
- [[ACL12_ACL13_HANDOFF]]
