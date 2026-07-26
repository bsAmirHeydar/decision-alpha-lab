---
title: "Decision, ADR and Waiver Governance"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Decision, ADR and Waiver Governance

Material semantic ambiguity requires an ADR. Temporary inability to satisfy a structural gate may receive a waiver, but waivers may not permit future leakage, hidden execution authority, unknown deletion, or unverified semantic merge.

Every decision records source authority, affected identities, alternatives, compatibility impact, rollback and expiry. Open decisions block only the transitions they affect; they must not be filled with implementation guesses.
