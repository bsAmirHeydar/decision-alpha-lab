# Stage 10 — Product Hardening + Packaging + Release Build

## Objective

Stage 10 converts `gartal terminal` from a multi-module technical build into a controlled beta release candidate. The stage does not add new market logic. It hardens product behavior, release discipline, customer packaging, preset defaults, license hooks, and QA gates.

## Engineering scope

- Add product/release fields to the runtime config.
- Add `GartalNewsProduct.mqh` as the owner of release profiles and license hooks.
- Add strict release mode to clamp noisy diagnostics for customer builds.
- Add release badge and watermark support in the dashboard.
- Add beta/stable/live presets.
- Add customer installation documentation in English and Persian.
- Upgrade package script to produce customer-oriented release ZIPs.
- Add beta QA checklist and manifest template.

## Non-goals

- No real cryptographic licensing yet.
- No marketplace payment integration.
- No promise that compiled `.ex5` exists in source control.
- No change to parser, filter, alert, or timeline truth models.

## Release channels

| Channel | Use |
|---|---|
| DEV | internal coding and debug visibility |
| BETA | closed test with selected users |
| STABLE | paid/customer release candidate |
| INTERNAL | support/debug build |

## Gate doctrine

A stable release must not ship silently in sample-data mode. If strict release mode is enabled and the channel is stable, sample mode blocks init.

## Handoff

After Stage 10, the next engineering work is compile-error fixing in MetaEditor, real broker QA, screenshot capture, licensing implementation, and payment/customer delivery infrastructure.
