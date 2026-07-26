---
title: Report Security and Redaction
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-08, reporting]
---
# Report Security and Redaction

ACL-08 produces three closed audience profiles. Internal Research receives candidate and gate details. Executive receives answer-first aggregates without candidate identifiers. External Restricted receives only aggregate counts, limitations and authority denials.

Redaction is allow-list projection, not string deletion after rendering. The external view is scanned for setup, candidate and decision identifiers. Unknown audience profiles fail closed. Report text cannot request tools, alter policy or become executable instructions.
