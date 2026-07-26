---
title: "Legacy Alias and Artifact Locator"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Legacy Alias and Artifact Locator

Aliases map experiment codes, file paths, include paths, function names, chart-object prefixes, configuration keys and documentation slugs to canonical identities. Aliases are versioned and can be active, redirecting, deprecated, quarantined or retired.

The locator resolves identity to canonical artifact without scanning the repository by convention. This prevents old path names from becoming permanent domain truth.
