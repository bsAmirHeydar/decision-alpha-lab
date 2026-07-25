# RTHP AI-Engine Input Binding

## Purpose

This directory contains the context-owned, machine-readable inputs required to expose the canonical RTHP Context to the existing Strategy Factory / SAED / UCEE engine. It is an integration package, not a new engine, detector, trainer, dataset builder, validation framework, treatment factory, or runtime.

The canonical semantic package remains frozen at:

- Context: `CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1`
- Context version: `1.0.2`
- ACL-03 state: `CONTEXT_COMPILED`
- AI package: `rthp.cross_symbol_cycle_divergence@1.0.0`

## Architectural boundary

The package is deliberately outside the canonical Context root. ACL-03 source approval hashes the semantic Context directory. Adding training bindings inside that directory would invalidate the approved source snapshot. The correct location is the UCE-I16 generated-context layer plus the context-owned Python plugin and registry records.

No file under the shared engine namespaces is modified. The binding implements the existing `ContextPackage` interface and supplies only RTHP-specific descriptors, mappings, contracts, fixtures, and preflight evidence.

## Inputs supplied to the engine

### Context package

The RTHP package provides:

1. `ContextPackageManifest`
2. 31 known-time-safe feature descriptors
3. 5 representation view descriptors
4. 4 dependence-cluster rules
5. 30 task references
6. `observe(source_record)`
7. `build_feature_frame(observation, source_record)`

### Canonical source record

Each accepted source record is a confirmed RTHP occurrence produced by the canonical RTHP detector/ledger. It includes event identity, pair and role identity, family, cycle lineage, polarity, timing, history sufficiency, cycle completeness, freshness, reference state, source revision, content digest, and exact auxiliary projection data.

The adapter does not detect divergence. It rejects records that do not satisfy the canonical source schema and Context invariants.

### Feature contract

The feature catalog exposes categorical, temporal, structural, and data-quality fields known at the RTHP observation cut. Raw symbol identifiers remain lineage metadata and are not emitted as trainable features. Optional price geometry is represented as explicit missingness when absent; it is never fabricated or silently imputed.

### Views

- `rthp.tabular.v1`
- `rthp.sparse_event.v1`
- `rthp.sequence.v1`
- `rthp.intermarket.v1`
- `rthp.graph.v1`

The package uses the existing shared view compilers. The intermarket view preserves Hunter/Protected roles and excludes raw symbol identity from the model payload.

### Dependence clusters

The package declares opportunity, shared-reference, symbol-pair/trading-day, and overlapping-outcome-path clusters. Shared split and validation systems consume these assignments to prevent sibling leakage and repeated counting of the same causal episode.

### Research tasks and labels

Task references cover factual reference exhaustion, polarity-signed forward response, polarity alignment, MFE, MAE, survival, family strength, and reference-age effectiveness. Label definitions are post-cut research templates and are never Context features. They are materialized only after ACL-05 freezes real source artifacts, horizons, maturity, censoring, splits, and search authority.

## Data modes

### Smoke mode

The smoke binding is deterministic, fixture-only, non-alpha evidence. It proves package registration, source validation, observation mapping, feature materialization, view compilation, cluster assignment, UCE-I16 generation, and causal conformance.

### Real research mode

Real training remains fail-closed until four external immutable sources are resolved:

1. Canonical RTHP occurrence ledger
2. RTHP reference-state ledger
3. RTHP cycle-instance ledger
4. Role-local price-path ledger for labels only

The real binding must include immutable artifact URIs, content hashes, provider and entitlement metadata, symbol pair, date range, New York time policy, price basis, tick-size source, rollover policy, producer version, and availability-time policy.

## Causality rules

- `observation_cut_ms` is the feature cut.
- No feature may have a known time after the cut.
- Post-cut prices are label-only.
- Unmatured outcomes are masked or censored.
- Future perturbation must not change past observation or feature hashes.
- Corrections append superseding observations; history is not overwritten.
- Stale or imputed records cannot masquerade as confirmed canonical occurrences.

## Commands

Smoke preflight:

```powershell
$env:PYTHONPATH = 'src\engine\packages'
python -m strategy_factory_rthp_context_v1.preflight `
  --source-jsonl 'contexts\legacy\strategy_factory\generated\rthp_cross_symbol_cycle_divergence\ai_input\fixtures\rthp_ai_smoke_records.jsonl' `
  --output 'artifacts\rthp\smoke_preflight.json'
```

Real-data readiness check:

```powershell
$env:PYTHONPATH = 'src\engine\packages'
python -m strategy_factory_rthp_context_v1.preflight `
  --source-jsonl '<REAL_CANONICAL_OCCURRENCE_JSONL>' `
  --real-data-binding '<RESOLVED_REAL_BINDING_JSON>' `
  --require-real-data `
  --output 'artifacts\rthp\real_preflight.json'
```

A successful real preflight authorizes entry into the existing shared train pipeline only to the extent granted by the frozen ACL-05 batch. It does not authorize treatment, orders, capital, or production promotion.
